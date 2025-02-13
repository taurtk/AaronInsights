from collections import defaultdict

class IdeaGenerator:
    def __init__(self):
        self.problem_indicators = [
            "need", "wish", "problem", "difficult", "hate", "annoying",
            "frustrated", "challenge", "improve", "better"
        ]
    
    def generate_ideas(self, posts, keywords):
        """Generate business ideas based on Reddit posts and keywords."""
        ideas = []
        problem_counts = defaultdict(int)
        
        # Analyze posts for common problems and patterns
        for post in posts:
            text = (post['title'] + " " + post['selftext']).lower()
            
            for indicator in self.problem_indicators:
                if indicator in text:
                    # Extract the sentence containing the problem indicator
                    sentences = text.split('.')
                    for sentence in sentences:
                        if indicator in sentence:
                            problem = sentence.strip()
                            problem_counts[problem] += post['score']
        
        # Generate ideas based on top problems
        sorted_problems = sorted(
            problem_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        for problem, score in sorted_problems[:5]:
            idea = {
                'problem': problem,
                'relevance_score': score,
                'potential_solution': self._generate_solution(problem, keywords)
            }
            ideas.append(idea)
        
        return ideas
    
    def _generate_solution(self, problem, keywords):
        """Generate a potential solution based on the problem and keywords."""
        # Simple template-based solution generation
        solution_templates = [
            "Create a platform that helps users {action} {target}",
            "Develop an app that simplifies {problem_area}",
            "Build a service that connects {user_type} with {solution_type}"
        ]
        
        # Basic solution generation logic
        if "need" in problem:
            return solution_templates[0].format(
                action="find",
                target="solutions quickly"
            )
        elif "difficult" in problem:
            return solution_templates[1].format(
                problem_area="this process"
            )
        else:
            return solution_templates[2].format(
                user_type="users",
                solution_type="service providers"
            )
