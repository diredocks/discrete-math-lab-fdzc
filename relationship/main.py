# main.py
from relationship import Relationship

def generate_circles(users, rel):
    """
    Generate social circles based on users and their following relationships.
    If user A follows B or B follows A, they are considered in the same circle.
    This function uses DFS to traverse an undirected graph and extract all connected components (social circles).

    Parameters:
        users: List of all usernames.
        rel: An instance of Relationship that stores following relationships.

    Returns:
        circles: A list of social circles, where each circle is a sorted list of usernames.
    """
    # Initialize an undirected graph: each user is a key with an empty set as its value.
    graph = {user: set() for user in users}
    
    # Build graph edges based on following relationships (bidirectional).
    for user in users:
        for friend in rel.followings_of(user):
            if friend in graph:
                # Establish a bidirectional connection between user and friend.
                graph[user].add(friend)
                graph[friend].add(user)
    
    visited = set()  # Set to keep track of visited users to avoid duplicates.
    circles = []     # List to store each social circle (as a list of users).
    
    # Use DFS to traverse each user.
    for user in users:
        if user not in visited:
            # If the user has not been visited, start a new circle from this user.
            stack = [user]
            circle = []
            while stack:
                u = stack.pop()
                if u not in visited:
                    visited.add(u)
                    circle.append(u)
                    # Add unvisited neighboring users to the stack.
                    stack.extend(graph[u] - visited)
            # Sort the current circle's members for consistent output.
            circles.append(sorted(circle))
    
    # Sort all circles based on the lexicographical order of the first member in each circle.
    circles.sort(key=lambda x: x[0])
    return circles

def main():
    """
    Main function:
    1. Reads the number of users and their usernames from the command line.
    2. Reads the number of following relationships and constructs the Relationship instance.
    3. Based on the entered command, performs one of the following operations:
       - Query Following: Outputs the target user's list of followed friends.
       - Friend Recommendation: Outputs a list of recommended friends for the target user.
       - Generate Circles: Outputs social circle information.
    """
    # 1. Read the number of users.
    n = int(input("Enter the number of users: ").strip())
    users = []  # List to store all usernames.
    print("Enter each username:")
    for _ in range(n):
        user = input().strip()  # Read and trim each username.
        users.append(user)
    
    # 2. Read the number of following relationships and build the relationships.
    m = int(input("Enter the number of following relationships: ").strip())
    # Create a Relationship instance to manage user following relationships.
    rel = Relationship()
    # Initialize each user in the relationship dictionary to ensure all users are present.
    for user in users:
        rel.relationship[user] = rel.followings_of(user)
    
    print("Enter each following relationship (format: username1 username2, meaning username1 follows username2):")
    for _ in range(m):
        line = input().strip()  # Read a line, for example, "A B".
        a, b = line.split()     # Split the line into two usernames.
        rel.follow(a, [b])      # Record that user a follows user b.
    
    # 3. Read the command from the user and execute the corresponding operation.
    print("Enter the command:")
    print("For example: 'Query Following username', 'Friend Recommendation username', or 'Generate Circles'")
    op_line = input().strip()  # Read the complete command line.
    
    # Determine which operation to execute based on the command.
    if op_line.startswith("Query Following"):
        # If the command is "Query Following", extract the target username.
        parts = op_line.split()
        if len(parts) == 2:
            target = parts[1]
        else:
            # If the target username is not provided in the command, prompt for it.
            target = input("Enter the target username: ").strip()
        # Retrieve the list of friends that the target user follows.
        followings = rel.followings_of(target)
        if followings:
            # Output the following list separated by commas if not empty.
            print("Following list: ", ",".join(followings))
        else:
            # Output a message if the user is not following anyone.
            print("This user is not following anyone.")
    
    elif op_line.startswith("Friend Recommendation"):
        # If the command is "Friend Recommendation", extract the target username.
        parts = op_line.split()
        if len(parts) == 2:
            target = parts[1]
        else:
            target = input("Enter the target username: ").strip()
        # Get friend recommendations for the target user.
        recommendations = rel.recommend(target)
        if recommendations:
            # Output the recommendations if available.
            print("Recommended friends: ", ",".join(recommendations))
        else:
            # Output a message if there are no suitable recommendations.
            print("No suitable friend recommendations for this user.")
    
    elif op_line.startswith("Generate Circles"):
        # If the command is "Generate Circles", generate social circles using the generate_circles function.
        circles = generate_circles(users, rel)
        # Print each circle with its index, member count, and member list.
        for i, circle in enumerate(circles, 1):
            print(f"Circle {i} ({len(circle)} members): {','.join(circle)}")
    else:
        # If the command does not match any known operation, output an error message.
        print("Unknown command.")

if __name__ == "__main__":
    # Entry point: when this script is executed as the main program, call the main() function.
    main()
