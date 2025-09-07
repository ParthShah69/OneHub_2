import React, { useState, useEffect } from 'react';
import './WeatherDashboard.css';

const WeatherDashboard = () => {
    const [weatherData, setWeatherData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [city, setCity] = useState('London');
    const [searchCity, setSearchCity] = useState('');
    const [isSearching, setIsSearching] = useState(false);

    const fetchWeatherData = async (cityName = city) => {
        if (cityName === city && !isSearching) {
            setLoading(true);
        } else {
            setIsSearching(true);
        }
        setError(null);
        
        // Update the city state immediately when searching to show correct loading text
        if (cityName !== city) {
            setCity(cityName);
        }
        
        try {
            const token = localStorage.getItem('auth_token');
            const response = await fetch(`http://localhost:5000/api/weather?city=${encodeURIComponent(cityName)}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `Failed to fetch weather for ${cityName}`);
            }

            const data = await response.json();
            setWeatherData(data);
            setError(null);
        } catch (err) {
            setError(err.message);
            console.error('Weather fetch error:', err);
        } finally {
            setLoading(false);
            setIsSearching(false);
        }
    };

    useEffect(() => {
        fetchWeatherData();
    }, []);

    const handleSearch = (e) => {
        e.preventDefault();
        if (searchCity.trim()) {
            fetchWeatherData(searchCity.trim());
            setSearchCity('');
        }
    };

    const getWeatherIcon = (iconCode) => {
        if (!iconCode) return 'https://openweathermap.org/img/wn/01d@2x.png';
        return `https://openweathermap.org/img/wn/${iconCode}@2x.png`;
    };

    const formatTemperature = (temp) => {
        return Math.round(temp || 0);
    };

    if (loading) {
        return (
            <div className="weather-dashboard">
                <div className="weather-header">
                    <h1>Weather Dashboard</h1>
                </div>
                <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <p>Loading weather data...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="weather-dashboard">
                <div className="weather-header">
                    <h1>Weather Dashboard</h1>
                </div>
                <div className="error-container">
                    <p className="error-message">Error: {error}</p>
                    <button onClick={() => fetchWeatherData()} className="retry-btn">
                        Try Again
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="weather-dashboard">
            <div className="weather-header">
                <h1>Weather Dashboard</h1>
                <form onSubmit={handleSearch} className="search-form">
                    <input
                        type="text"
                        placeholder="Enter city name..."
                        value={searchCity}
                        onChange={(e) => setSearchCity(e.target.value)}
                        className="city-input"
                    />
                    <button type="submit" className="search-btn">Search</button>
                </form>
            </div>

            {isSearching && (
                <div className="search-loading">
                    <div className="loading-spinner small"></div>
                    <p>Searching for {city}...</p>
                </div>
            )}

            {weatherData && !isSearching && (
                <>
                    <div className="current-weather">
                        <div className="current-info">
                            <div className="location">
                                <h2>{weatherData.city}{weatherData.country && `, ${weatherData.country}`}</h2>
                                {weatherData.is_mock && <span className="mock-badge">Demo Data</span>}
                                {!weatherData.is_mock && <span className="live-badge">Live Data</span>}
                            </div>
                            <div className="temperature">
                                <span className="temp-value">{formatTemperature(weatherData.temperature)}°C</span>
                                <img 
                                    src={getWeatherIcon(weatherData.icon)} 
                                    alt={weatherData.description}
                                    className="weather-icon"
                                />
                            </div>
                        </div>
                        <div className="weather-details">
                            <p className="description">{weatherData.description}</p>
                            {weatherData.feels_like && (
                                <p className="feels-like">Feels like {formatTemperature(weatherData.feels_like)}°C</p>
                            )}
                            <div className="details-grid">
                                <div className="detail-item">
                                    <span className="label">Humidity</span>
                                    <span className="value">{weatherData.humidity}%</span>
                                </div>
                                <div className="detail-item">
                                    <span className="label">Wind Speed</span>
                                    <span className="value">{weatherData.wind_speed} km/h</span>
                                </div>
                                {weatherData.pressure && (
                                    <div className="detail-item">
                                        <span className="label">Pressure</span>
                                        <span className="value">{weatherData.pressure} hPa</span>
                                    </div>
                                )}
                                {weatherData.visibility && (
                                    <div className="detail-item">
                                        <span className="label">Visibility</span>
                                        <span className="value">{weatherData.visibility} km</span>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>

                    {weatherData.forecast && weatherData.forecast.length > 0 && (
                        <div className="forecast-section">
                            <h3>5-Day Forecast</h3>
                            <div className="forecast-grid">
                                {weatherData.forecast.map((day, index) => (
                                    <div key={index} className="forecast-card">
                                        <div className="forecast-day">{day.day}</div>
                                        <img 
                                            src={getWeatherIcon(day.icon)} 
                                            alt={day.description}
                                            className="forecast-icon"
                                        />
                                        <div className="forecast-temps">
                                            <span className="high">{formatTemperature(day.high)}°</span>
                                            <span className="low">{formatTemperature(day.low)}°</span>
                                        </div>
                                        <div className="forecast-desc">{day.description}</div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </>
            )}
        </div>
    );
};

export default WeatherDashboard;
