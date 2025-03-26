import relationship

def main():

    # Step 1: Read the number of users and collect their usernames.
    n = int(input("Enter the number of users: ").strip())
    users = []
    print("Enter each username:")
    for _ in range(n):
        user = input().strip()
        users.append(user)
    
    # Step 2: Initialize the Relationship instance and ensure each user is in the relation.
    rel = relationship.Relationship()
    for user in users:
        if user not in rel.relationship:
            rel.relationship[user] = []  # Initialize with an empty list if not already present.
    
    # Read the number of follow relationships.
    m = int(input("Enter the number of follow relationships: ").strip())
    print("Enter each follow relationship (format: follower followee):")
    for _ in range(m):
        line = input().strip()
        follower, followee = line.split()
        rel.follow(follower, [followee])
    
    # Interactive menu loop.
    while True:
        print("\nPlease choose an option:")
        print("1. Query Following")
        print("2. Recommend Friends")
        print("3. Generate Social Circles")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            # Query the following list for a given user.
            target_user = input("Enter the target user: ").strip()
            following_list = rel.followings_of(target_user)
            if following_list:
                print("Following list: " + ", ".join(following_list))
            else:
                print("This user is not following anyone.")
        
        elif choice == "2":
            # Recommend friends for a given user.
            target_user = input("Enter the target user: ").strip()
            recommended_friends = rel.recommend(target_user)
            if recommended_friends:
                print("Recommended friends: " + ", ".join(recommended_friends))
            else:
                print("No suitable friend recommendations for this user.")
        
        elif choice == "3":
            # Generate social circles using the generate_circles method in Relationship class.
            circles = rel.generate_circles(users)
            if circles:
                for idx, circle in enumerate(circles, start=1):
                    sorted_circle = sorted(circle)
                    print(f"Circle {idx} ({len(sorted_circle)} members): " + ", ".join(sorted_circle))
            else:
                print("No social circles could be generated.")
        
        elif choice == "4":
            print("Exiting the program.")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()