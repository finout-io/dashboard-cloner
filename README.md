# Finout Dashboard Cloner

   This project is a Streamlit application that allows users to quickly clone dashboards to other accounts, maintaining all relevent widgets and placement.

   ![Alt text](assets/cloner.png "1")

## Requirements

- Python 3.7 or higher
- Streamlit

## Installation

Clone the repository
Install the required packages using pip:

   ```sh
   pip install -r requirements.txt
   ```

## Running the Application

To run the application, use the following command:

```sh
streamlit run app.py
```

## Form Fields

- **Source Account ID**: Account ID of the source you want to clone **from**.
- **Source Dashboard ID**: ID of Dashboard you want to clone.
- **Target Account ID**: Account ID of the target you want to clone **to**
- **New Dashboard Name**: Name your new dashboard

## Usage

1. **Connect to VPN**
2. **Fill Out the Form**: Enter values for all fields.
3. **Submit the Form**: Click the "Submit" button to submit the form.
4. **Validate in Finout**: Once submitted with a success message, check the **target** finout tenant for the cloned dashboard.


## Issues and Contributions

If you encounter any issues, feel free to open an issue in the repository. Contributions are welcome to improve the project.