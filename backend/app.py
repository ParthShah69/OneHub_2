from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import requests
import time
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)

# Configuration
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '46575fbd9144430bb7dce528004ec99e')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', 'AIzaSyDBGtdTras52CsvF5X8QEk6vpM9vhiQYxo')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', 'aWGR_XGyaWsFm2MXrY_X-Q')
REDDIT_SECRET = os.getenv('REDDIT_SECRET', 'zXUAt78OltVuLnymF2qc-bDkCWEZyA')
ADZUNA_APP_ID = os.getenv('ADZUNA_APP_ID', 'your_adzuna_app_id_here')
ADZUNA_APP_KEY = os.getenv('ADZUNA_APP_KEY', 'your_adzuna_app_key_here')

# Health check endpoint
@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "dashboard-backend"})

# News Service Endpoints
@app.route('/api/news')
def get_news():
    category = request.args.get('category', 'general')
    
    if not NEWS_API_KEY or NEWS_API_KEY == 'your_newsapi_key_here':
        # Return mock data
        articles = [
            {
                "id": f"news_{int(time.time())}",
                "title": f"⚠️ MOCK DATA: Latest {category.title()} News",
                "description": f"This is mock data for {category}. Add NEWS_API_KEY to get real news.",
                "url": "https://newsapi.org/register",
                "source": "Mock Data - Add API Key",
                "category": category,
                "published_at": datetime.now().isoformat(),
                "image_url": "https://via.placeholder.com/300x200/ff6b6b/ffffff?text=MOCK+DATA",
                "is_static": True
            }
        ]
        return jsonify({
            "category": category,
            "count": len(articles),
            "articles": articles,
            "message": "Add NEWS_API_KEY to get real data"
        })
    
    # Real NewsAPI call
    try:
        url = f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={NEWS_API_KEY}&pageSize=20"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = []
            
            for article in data.get('articles', []):
                articles.append({
                    "id": f"news_{int(time.time())}_{len(articles)}",
                    "title": article.get('title', ''),
                    "description": article.get('description', ''),
                    "url": article.get('url', ''),
                    "source": article.get('source', {}).get('name', ''),
                    "category": category,
                    "published_at": article.get('publishedAt', ''),
                    "image_url": article.get('urlToImage', ''),
                    "is_static": False
                })
            
            return jsonify({
                "category": category,
                "count": len(articles),
                "articles": articles,
                "source": "NewsAPI"
            })
        else:
            raise Exception(f"API returned status {response.status_code}")
            
    except Exception as e:
        # Fallback to mock data on error
        return jsonify({
            "category": category,
            "count": 1,
            "articles": [{
                "id": f"error_{int(time.time())}",
                "title": f"Error fetching {category} news",
                "description": f"API Error: {str(e)}. Showing mock data.",
                "url": "#",
                "source": "Error Fallback",
                "category": category,
                "published_at": datetime.now().isoformat(),
                "image_url": "https://via.placeholder.com/300x200/orange/white?text=API+ERROR",
                "is_static": True
            }],
            "error": str(e)
        })

@app.route('/api/news/trending')
def get_trending_news():
    categories = ['technology', 'business', 'entertainment', 'sports']
    all_articles = []
    
    for category in categories:
        try:
            if NEWS_API_KEY and NEWS_API_KEY != 'your_newsapi_key_here':
                url = f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={NEWS_API_KEY}&pageSize=5"
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    for article in data.get('articles', []):
                        all_articles.append({
                            "id": f"trending_{int(time.time())}_{len(all_articles)}",
                            "title": article.get('title', ''),
                            "description": article.get('description', ''),
                            "url": article.get('url', ''),
                            "source": article.get('source', {}).get('name', ''),
                            "category": category,
                            "published_at": article.get('publishedAt', ''),
                            "image_url": article.get('urlToImage', ''),
                        })
        except:
            # Add mock data for failed categories
            all_articles.append({
                "id": f"mock_trending_{category}_{int(time.time())}",
                "title": f"Trending {category.title()} News",
                "description": f"Latest updates in {category}",
                "url": "#",
                "source": "Mock Source",
                "category": category,
                "published_at": datetime.now().isoformat(),
                "image_url": "https://via.placeholder.com/300x200",
            })
    
    return jsonify({
        "count": len(all_articles),
        "articles": all_articles
    })

@app.route('/api/news/search')
def search_news():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    
    # Mock search results
    articles = [{
        "id": f"search_{int(time.time())}",
        "title": f"Search Results for: {query}",
        "description": f"Latest news and updates related to {query}",
        "url": "#",
        "source": "Search Results",
        "category": "search",
        "published_at": datetime.now().isoformat(),
        "image_url": "https://via.placeholder.com/300x200",
    }]
    
    return jsonify({
        "query": query,
        "count": len(articles),
        "articles": articles
    })

# Jobs Service Endpoints
@app.route('/api/jobs')
def get_jobs():
    category = request.args.get('category', 'technology')
    
    # Mock job data
    jobs = [
        {
            "id": f"job_{int(time.time())}",
            "title": f"Senior {category.title()} Engineer",
            "company": "Tech Corp Inc.",
            "location": "San Francisco, CA",
            "type": "Full-time",
            "salary": "$120,000 - $180,000",
            "description": f"We are looking for a talented {category} professional to join our team.",
            "url": "https://example.com/jobs/1",
            "category": category,
            "posted_at": (datetime.now() - timedelta(hours=24)).isoformat(),
            "is_static": True
        },
        {
            "id": f"job_{int(time.time())}_2",
            "title": f"{category.title()} Specialist",
            "company": "Innovation Labs",
            "location": "Remote",
            "type": "Contract",
            "salary": "$80 - $120/hour",
            "description": f"Remote {category} position with flexible hours.",
            "url": "https://example.com/jobs/2",
            "category": category,
            "posted_at": (datetime.now() - timedelta(hours=12)).isoformat(),
            "is_static": True
        }
    ]
    
    return jsonify({
        "category": category,
        "count": len(jobs),
        "jobs": jobs,
        "message": "Add ADZUNA_APP_ID and ADZUNA_APP_KEY for real job data"
    })

@app.route('/api/jobs/trending')
def get_trending_jobs():
    jobs = [
        {
            "id": f"trending_job_{int(time.time())}",
            "title": "AI/ML Engineer",
            "company": "AI Startup Co.",
            "location": "Remote",
            "description": "Join our AI team to build cutting-edge machine learning solutions.",
            "url": "https://example.com/jobs/ai",
            "category": "ai",
            "posted_at": (datetime.now() - timedelta(hours=12)).isoformat(),
            "salary": "$100,000 - $150,000",
        },
        {
            "id": f"trending_job_{int(time.time())}_2",
            "title": "Cloud Solutions Architect",
            "company": "CloudTech Solutions",
            "location": "New York, NY",
            "description": "Design and implement cloud infrastructure solutions.",
            "url": "https://example.com/jobs/cloud",
            "category": "cloud",
            "posted_at": (datetime.now() - timedelta(hours=6)).isoformat(),
            "salary": "$130,000 - $200,000",
        }
    ]
    
    return jsonify({
        "count": len(jobs),
        "jobs": jobs
    })

@app.route('/api/jobs/search')
def search_jobs():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    
    jobs = [{
        "id": f"search_job_{int(time.time())}",
        "title": f"Jobs matching: {query}",
        "company": "Various Companies",
        "location": "Multiple Locations",
        "description": f"Job opportunities related to {query}",
        "url": "#",
        "category": "search",
        "posted_at": datetime.now().isoformat(),
        "salary": "Competitive",
    }]
    
    return jsonify({
        "query": query,
        "count": len(jobs),
        "jobs": jobs
    })

# Videos Service Endpoints
@app.route('/api/videos')
def get_videos():
    category = request.args.get('category', 'technology')
    
    videos = [
        {
            "id": f"video_{int(time.time())}",
            "title": f"Latest {category.title()} Trends",
            "description": f"Comprehensive overview of {category} developments",
            "url": "https://youtube.com/watch?v=example1",
            "thumbnail": "https://via.placeholder.com/480x360",
            "channel": "Tech Channel",
            "category": category,
            "published_at": (datetime.now() - timedelta(days=1)).isoformat(),
            "duration": "10:30",
            "views": "125K"
        },
        {
            "id": f"video_{int(time.time())}_2",
            "title": f"{category.title()} Tutorial",
            "description": f"Step-by-step guide to {category}",
            "url": "https://youtube.com/watch?v=example2",
            "thumbnail": "https://via.placeholder.com/480x360",
            "channel": "Learn Channel",
            "category": category,
            "published_at": (datetime.now() - timedelta(hours=12)).isoformat(),
            "duration": "15:45",
            "views": "89K"
        }
    ]
    
    return jsonify({
        "category": category,
        "count": len(videos),
        "videos": videos
    })

# Deals Service Endpoints
@app.route('/api/deals')
def get_deals():
    category = request.args.get('category', 'electronics')
    
    deals = [
        {
            "id": f"deal_{int(time.time())}",
            "title": f"Amazing {category.title()} Deal",
            "description": f"Great discount on {category} items",
            "url": "https://example.com/deals/1",
            "platform": "Amazon",
            "category": category,
            "price": 79.99,
            "original_price": 129.99,
            "discount": 38.46,
            "image_url": "https://via.placeholder.com/300x200",
            "valid_until": (datetime.now() + timedelta(days=7)).isoformat()
        },
        {
            "id": f"deal_{int(time.time())}_2",
            "title": f"{category.title()} Special Offer",
            "description": f"Limited time offer on {category}",
            "url": "https://example.com/deals/2",
            "platform": "Flipkart",
            "category": category,
            "price": 299.99,
            "original_price": 399.99,
            "discount": 25.0,
            "image_url": "https://via.placeholder.com/300x200",
            "valid_until": (datetime.now() + timedelta(days=5)).isoformat()
        }
    ]
    
    return jsonify({
        "category": category,
        "count": len(deals),
        "deals": deals
    })

# User Service Endpoints
@app.route('/api/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    
    user = {
        "id": f"user_{int(time.time())}",
        "email": user_data.get('email', 'user@example.com'),
        "name": user_data.get('name', 'Demo User'),
        "interests": user_data.get('interests', ['technology', 'ai', 'business']),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    return jsonify(user)

@app.route('/api/users/<user_id>')
def get_user(user_id):
    user = {
        "id": user_id,
        "email": "user@example.com",
        "name": "Demo User",
        "interests": ["technology", "ai", "business"],
        "created_at": (datetime.now() - timedelta(days=30)).isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    return jsonify(user)

# Recommendations Service
@app.route('/api/recommendations')
def get_recommendations():
    user_id = request.args.get('user_id', 'default_user')
    
    recommendations = [
        {
            "id": f"rec_{int(time.time())}",
            "type": "news",
            "title": "AI Breakthrough in Healthcare",
            "description": "Latest AI developments",
            "url": "/api/news",
            "category": "technology",
            "score": 0.95
        },
        {
            "id": f"rec_{int(time.time())}_2",
            "type": "job",
            "title": "Senior Developer Position",
            "description": "Great opportunity in tech",
            "url": "/api/jobs",
            "category": "technology",
            "score": 0.88
        }
    ]
    
    return jsonify({
        "user_id": user_id,
        "count": len(recommendations),
        "recommendations": recommendations
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
