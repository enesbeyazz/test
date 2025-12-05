import datetime 
from typing import List, Dict, Optional 

class Interaction:
    """Represents a single interaction event on a post"""
    def __init__(self, interaction_id, interaction_type:str, post, source_account=None):
        self.id = interaction_id
        self.type = interaction_type # 'like', 'comment', 'share', 'view'
        self.post = post 
        self.timestamp = datetime.datetime.now()
        self.source_account = source_account  # Optional: who interacted

class SocialAccount: 
    """Represents a social media account on any platform"""
    def __init__(self, account_id: int, username: str , platform:str):
        self.id = account_id
        self.username = username
        self.platform = platform
        self.followers_count = 0
        self.following_count = 0
        self.posts: List['SocialPost'] = []

    def view_profile(self) -> str:
        return f"Username: {self.username}, Platform: {self.platform}, Followers: {self.followers_count}, Following: {self.following_count}"

class SocialPost:
    """Represents a generic post across platforms"""
    def __init__(self, post_id:int , content:str, account: SocialAccount):
        self.id = post_id
        self.content = content 
        self.account = account 
        self.timestamp = datetime.datetime.now()
        # Aggregated metrics
        self.likes = 0
        self.comments = 0
        self.shares = 0
        self.impressions = 0
        self.interactions = []
         # Store all interactions

    def add_like(self, source_account=None):
        self.likes += 1 
        interaction = Interaction(len(self.interactions) + 1, 'like', self, source_account)
        self.interactions.append(interaction)

    def add_comment(self, source_account = None):
        self.comments += 1 
        interaction = Interaction(len(self.interactions) + 1, 'comment', self, source_account)
        self.interactions.append(interaction)

    def add_share(self, source_account=None):
        self.shares += 1
        interaction = Interaction(len(self.interactions) + 1, 'share', self, source_account)
        self.interactions.append(interaction)

    def add_impression(self):
        self.impressions += 1
        interaction = Interaction(len(self.interactions) + 1, 'view', self)
        self.interactions.append(interaction)


class AnalyticsEngine:
    """Central class for computing metrics and summaries"""
    
    def calculate_engagement_rate(self, post:SocialPost) -> float:
        """Calculate engagement rate: (likes + comments + shares) / followers"""
        total_interaction = post.likes + post.comments + post.shares
        followers = post.account.followers_count

        if followers == 0:
            return 0.0
            
        return total_interaction / followers
        
    def get_account_summary(self, account: SocialAccount) -> Dict:
        """Get summary statistics for an account"""
        total_likes = sum(post.likes for post in account.posts)
        total_comments = sum(post.comments for post in account.posts)
        total_shares = sum(post.shares for post in account.posts)
        total_impressions = sum(post.impressions for post in account.posts)

        return {
            'username': account.username,
            'platform': account.platform,
            'total_posts': len(account.posts),
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_shares': total_shares,
            'total_impressions': total_impressions
        }
      
class SocialMediaAnalyticsSystem:
    """High-level orchestrator for the analytics system"""
    def __init__(self):
        self.accounts: List[SocialAccount] = [] 
        self.posts: List[SocialPost] = []
        self.analytics_engine = AnalyticsEngine()
        # Hash maps for fast lookup 
        self.accounts_by_id: Dict[int, SocialAccount] = {}
        self.posts_by_id: Dict[int, SocialPost] = {}

    def add_account(self, account: SocialAccount):
        """Add a social account to the system"""
        self.accounts.append(account)
        self.accounts_by_id[account.id] = account

    def add_post(self, post: SocialPost):
        """Add a post to the system""" 
        self.posts.append(post)
        self.posts_by_id[post.id] = post
        post.account.posts.append(post) 
        
    def get_post_by_id(self, post_id: int) -> Optional[SocialPost]:
        """Fast lookup of post by ID"""
        return self.posts_by_id.get(post_id)

    def get_account_by_id(self, account_id: int) -> Optional[SocialAccount]:
        """Fast lookup of account by ID"""
        return self.accounts_by_id.get(account_id)

    def get_top_posts_by_engagement(self, limit: int = 10) -> List[SocialPost]:
        """Get top posts ranked by engagement rate"""
        sorted_posts = sorted(
            self.posts,
            key=lambda p: self.analytics_engine.calculate_engagement_rate(p),
            reverse=True
        )
        return sorted_posts[:limit]

    def get_account_summary(self, account_id: int) -> Optional[Dict]:
        """Get summary statistics for an account"""
        account = self.get_account_by_id(account_id)
        if not account:
            return None
        return self.analytics_engine.get_account_summary(account)

# Example usage
if __name__ == "__main__":
    print("System is starting...")
    system = SocialMediaAnalyticsSystem()
    
    # Create account
    user1 = SocialAccount(1, "hz.enes_official", "Instagram")
    user1.followers_count = 1500
    system.add_account(user1)
    
    # Create post
    post1 = SocialPost(101, "Respect to hz_enes", user1)
    system.add_post(post1)
    
    # Add interactions
    post1.add_like()
    post1.add_like()
    post1.add_comment()
    post1.add_share()
    post1.add_impression()
    
    # Get analytics
    engagement = system.analytics_engine.calculate_engagement_rate(post1)
    summary = system.get_account_summary(1)
    
    print(f"Engagement Rate: {engagement:.2%}")
    print(f"Account Summary: {summary}")
    print("test")