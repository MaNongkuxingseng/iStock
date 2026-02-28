use reqwest;
use serde::{Deserialize, Serialize};
use std::time::Duration;

// Response structure for Open-Meteo API
#[derive(Deserialize, Debug)]
struct WeatherResponse {
    #[serde(rename = "current")]
    current_weather: CurrentWeather,
}

#[derive(Deserialize, Debug)]
struct CurrentWeather {
    #[serde(rename = "temperature_2m")]
    temperature_2m: f64,
    #[serde(rename = "time")]
    time: String,
}

/// Fetches current weather temperature in Celsius from Open-Meteo API
/// 
/// # Arguments
/// * `latitude` - Latitude coordinate (e.g., 51.5074 for London)
/// * `longitude` - Longitude coordinate (e.g., -0.1278 for London)
/// 
/// # Returns
/// * `Result<f64, Box<dyn std::error::Error>>` - Temperature in Celsius or error
/// 
/// # Example
/// ```
/// let temp = fetch_weather_temperature(51.5074, -0.1278).await?;
/// println!("Current temperature: {}°C", temp);
/// ```
async fn fetch_weather_temperature(
    latitude: f64,
    longitude: f64,
) -> Result<f64, Box<dyn std::error::Error>> {
    // Build the Open-Meteo API URL
    let url = format!(
        "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current=temperature_2m&temperature_unit=celsius&timezone=auto",
        latitude, longitude
    );
    
    // Create HTTP client with timeout
    let client = reqwest::Client::builder()
        .timeout(Duration::from_secs(30))
        .build()?;
    
    // Make the GET request
    let response = client.get(&url).send().await?;
    
    // Check if the request was successful
    if !response.status().is_success() {
        return Err(format!("API request failed with status: {}", response.status()).into());
    }
    
    // Parse the JSON response
    let weather_data: WeatherResponse = response.json().await?;
    
    Ok(weather_data.current_weather.temperature_2m)
}

// Example usage function (for testing)
#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_fetch_weather_temperature() {
        // Test with known coordinates (London)
        let result = fetch_weather_temperature(51.5074, -0.1278).await;
        assert!(result.is_ok());
        let temp = result.unwrap();
        // Temperature should be a reasonable value (-50 to 50°C)
        assert!(temp >= -50.0 && temp <= 50.0);
    }
}

// Example main function to demonstrate usage
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Example: Get temperature for Beijing (39.9042, 116.4074)
    match fetch_weather_temperature(39.9042, 116.4074).await {
        Ok(temp) => println!("Current temperature in Beijing: {:.1}°C", temp),
        Err(e) => eprintln!("Error fetching weather: {}", e),
    }
    
    Ok(())
}