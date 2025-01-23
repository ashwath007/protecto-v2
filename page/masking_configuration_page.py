import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from protectoMethods import ProtectoAPI

class MaskConfigPage:
    """
    A class to handle the mask configuration page in the Streamlit application.
    This class manages the display and interaction with a data masking configuration interface,
    allowing users to specify which fields should be masked and how they should be handled.
    """
    
    def __init__(self):
        """
        Initialize the MaskConfigPage with necessary API connections and data.
        Sets up the connection to the ProtectoAPI and retrieves the list of available objects.
        """
        self.protecto_api = ProtectoAPI()
        self.objects = self.protecto_api.get_list_of_objects()

    def _create_fields_table(self, fields_data):
        """
        Creates an interactive table using AgGrid to display and edit field metadata.
        
        Args:
            fields_data (list): List of dictionaries containing field metadata
            
        Returns:
            pandas.DataFrame: Updated DataFrame containing the modified field data
        """
        try:
            # Create initial DataFrame and print column names for debugging
            df = pd.DataFrame(fields_data)
            print("Initial DataFrame columns:", df.columns.tolist())
            
            # Define the standardized column names we want to use
            desired_columns = {
                'Field': ['field', 'Field'],
                'PII Identified': ['pii_identified', 'PII Identified'],
                'Override Pii': ['override_pii', 'Override Pii'],
                'To Be Masked': ['to_be_masked', 'To Be Masked'],
                'Samples': ['samples', 'Samples']
            }
            
            # Create a mapping dictionary based on actual column names
            column_mapping = {}
            for desired_col, possible_names in desired_columns.items():
                for col in df.columns:
                    if col.lower().replace(" ", "_") in [name.lower().replace(" ", "_") for name in possible_names]:
                        column_mapping[col] = desired_col
                        break
            
            # Rename the columns
            df = df.rename(columns=column_mapping)
            print("DataFrame columns after renaming:", df.columns.tolist())
            
            # Convert boolean values to Yes/No
            if 'To Be Masked' in df.columns:
                df['To Be Masked'] = df['To Be Masked'].map({True: 'Yes', False: 'No'})
            
            # Configure grid options
            gb = GridOptionsBuilder.from_dataframe(df)
            
            # Set default column properties
            gb.configure_default_column(
                editable=True,
                resizable=True,
                filterable=True,
                sorteable=True
            )
            
            # Configure specific columns
            if 'Field' in df.columns:
                gb.configure_column(
                    "Field",
                    editable=False,
                    width=150
                )
            
            if 'To Be Masked' in df.columns:
                gb.configure_column(
                    "To Be Masked",
                    cellEditor='agSelectCellEditor',
                    cellEditorParams={
                        'values': ['Yes', 'No']
                    },
                    cellStyle=JsCode("""
                        function(params) {
                            if (params.value === 'Yes') {
                                return {'backgroundColor': '#90EE90'};
                            } else {
                                return {'backgroundColor': '#FFB6C1'};
                            }
                        }
                    """),
                    width=120
                )
            
            if 'PII Identified' in df.columns:
                gb.configure_column(
                    "PII Identified",
                    editable=False,
                    width=150
                )
            
            if 'Override Pii' in df.columns:
                gb.configure_column(
                    "Override Pii",
                    cellEditor='agSelectCellEditor',
                    cellEditorParams={
                        'values': ["PERSON", "EMAIL", "NO PII", "URL", "ADDRESS", "PHONE"]
                    },
                    width=150
                )
            
            if 'Samples' in df.columns:
                gb.configure_column(
                    "Samples",
                    editable=False,
                    width=250
                )
            
            # Build grid options
            grid_options = gb.build()
            grid_options['domLayout'] = 'normal'
            
            # Create and display the AgGrid component
            grid_response = AgGrid(
                df,
                gridOptions=grid_options,
                height=400,
                allow_unsafe_jscode=True,
                theme='streamlit'
            )
            
            # Process the updated data
            updated_df = grid_response['data']
            
            # Convert Yes/No back to boolean values
            if updated_df is not None and 'To Be Masked' in updated_df.columns:
                updated_df['To Be Masked'] = updated_df['To Be Masked'].map({'Yes': True, 'No': False})
            
            return updated_df
            
        except Exception as e:
            st.error(f"An error occurred while creating the fields table: {str(e)}")
            print("Error details:", e)
            print("Available columns:", df.columns.tolist() if 'df' in locals() else "DataFrame not created")
            return None

    def show(self):
        """
        Displays the mask configuration page in the Streamlit application.
        This method handles the main UI layout and all user interactions.
        """
        # Configure the Streamlit page layout
        st.markdown("""
            <style>
            [data-testid="stAppViewContainer"] {
                padding-top: 0;
            }
            .block-container {
                padding-top: 1.0rem;
                max-width: 100%;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Set page title
        st.title("Mask Configuration")
        
        # Create layout columns
        col1, col2 = st.columns([1, 2])
        
        # Object selection dropdown
        with col1:
            try:
                selected_object = st.selectbox(
                    "Object",
                    [""] + self.objects,
                    key="mask_config_object",
                    index=1 + self.objects.index(st.session_state.selected_object)
                )
            except Exception as e:
                st.error(f"Error in object selection: {str(e)}")
                return
        
        try:
            # Fetch metadata for the selected object
            metadata = self.protecto_api.get_metadata_for_mask(st.session_state.selected_object)
            st.session_state.field_metadata = metadata.get('field_metadata', [])
            
            # Print the structure of field_metadata for debugging
            print("Field metadata structure:", 
                  [list(item.keys()) for item in st.session_state.field_metadata[:1]])
            
            st.session_state.show_table = True
            
            # Create main content container
            with st.container():
                # Display the fields table
                edited_fields = self._create_fields_table(st.session_state.field_metadata)
                
                # Create button container
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col2:
                        schedule_button = st.button("Schedule for masking", type="primary")
                
                # Handle scheduling button click
                if schedule_button and edited_fields is not None:
                    try:
                        fields_records = edited_fields.to_dict('records')
                        print("Updated fields records:", fields_records)
                        
                        # Update mask metadata through API
                        result = self.protecto_api.update_mask_metadata(
                            selected_object,
                            st.session_state.query,
                            fields_records
                        )
                        
                        # Handle API response
                        if result.get('is_rows_selected_for_masking'):
                            st.success(result.get('message'))
                            st.session_state.show_table = False
                            if 'field_metadata' in st.session_state:
                                del st.session_state.field_metadata
                        else:
                            st.error("Failed to update mask configuration. Please try again.")
                    except Exception as e:
                        st.error(f"Error updating mask configuration: {str(e)}")
                        
        except Exception as e:
            st.error(f"An error occurred while fetching metadata: {str(e)}")
            return

if __name__ == "__main__":
    mask_config_page = MaskConfigPage()
    mask_config_page.show()