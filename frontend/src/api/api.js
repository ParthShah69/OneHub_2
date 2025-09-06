const API_BASE_URL = 'http://localhost:5000';

class ApiService {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // News endpoints
  async getNews(category = 'general') {
    return this.request(`/api/news?category=${category}`);
  }

  async getTrendingNews() {
    return this.request('/api/news/trending');
  }

  async searchNews(query) {
    return this.request(`/api/news/search?q=${encodeURIComponent(query)}`);
  }

  // Jobs endpoints
  async getJobs(category = 'technology') {
    return this.request(`/api/jobs?category=${category}`);
  }

  async getTrendingJobs() {
    return this.request('/api/jobs/trending');
  }

  async searchJobs(query) {
    return this.request(`/api/jobs/search?q=${encodeURIComponent(query)}`);
  }

  // Videos endpoints
  async getVideos(category = 'technology') {
    return this.request(`/api/videos?category=${category}`);
  }

  // Deals endpoints
  async getDeals(category = 'electronics') {
    return this.request(`/api/deals?category=${category}`);
  }

  // User endpoints
  async createUser(userData) {
    return this.request('/api/users', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async getUser(userId) {
    return this.request(`/api/users/${userId}`);
  }

  // Recommendations endpoint
  async getRecommendations(userId = 'default_user') {
    return this.request(`/api/recommendations?user_id=${userId}`);
  }

  // Health check
  async healthCheck() {
    return this.request('/health');
  }
}

const apiService = new ApiService();
export default apiService;
