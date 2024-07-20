# Dubai Real Estate Streamlit App

This is a comprehensive dashboard for analyzing Dubai real estate data. The application allows users to visualize market trends, filter data by various parameters, and view transaction heat maps. The app includes an ETL process that updates the data weekly.

## Features

- **Market Size and Growth Analysis**: Visualize the market size and growth rate for different property types over the years.
- **Market Sale Price Analysis**: View detailed trends and changes in sale prices, including historical prices and heat maps.
- **Interactive Filters**: Filter data by date, area, property type, and number of rooms.
- **Heat Maps**: Visualize transactions across Dubai using interactive heat maps.

## Installation

### Using pip

1. **Clone the repository:**

    ```bash
    git clone https://github.com/alifadl009/Dubai-Real-Estate-App/
    cd dubai-real-estate-app
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the app:**

    ```bash
    streamlit run Overview.py
    ```

### Using Docker

1. **Build the Docker image:**

    ```bash
    docker build -t dubai-real-estate-app .
    ```

2. **Run the Docker container:**

    ```bash
    docker run -p 8501:8501 dubai-real-estate-app
    ```

3. **Access the app:**
    Open your browser and navigate to `http://localhost:8501`.

## Usage

Once the app is running, you can navigate through different sections:

1. **Market Size and Growth**: Use the sidebar filters to select the start year and parameters for analysis. Visualize the market size and growth rate using the provided graphs.

2. **Market Sale Price**: Use the sidebar filters to select the date range, area, property type, and number of rooms. View the sale price trends and heat maps.

## ETL Process

The app includes an ETL process that updates the real estate data weekly. The ETL script processes the data and stores it in a format ready for visualization. To run the ETL process:

1. **Activate your virtual environment:**

    ```bash
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. **Run the ETL script:**

    ```bash
    bash etl.sh
    ```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
