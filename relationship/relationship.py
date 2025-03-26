class Relationship:
    relationship = {}

    def follow(self, target_user, followings):
        # Create a follow in relationship
        current_followings = self.followings_of(target_user)
        self.relationship[target_user] = current_followings + [
            following for following in followings if following not in current_followings
        ]

    def followings_of(self, target_user):
        # This returns a list that contains
        # users followed by target_user
        return self.relationship.get(target_user, [])

    def followed_by(self, target_user):
        # This returns a list that contains
        # users that follows target_user
        return [
            user
            for user, followings in self.relationship.items()
            if target_user in followings
        ]

    def followings_followed(self, target_user, depth=1):
        # This returns a list that contains
        # those followings from users followed by target_user
        if depth <= 0:
            return self.followings_of(target_user)

        followings_follows = [
            user
            for following in self.followings_of(target_user)
            for user in self.followings_followed(following, depth - 1)
        ]

        return followings_follows

    def recommend(self, target_user):
        # Fisrt we recommend users following target_user
        # and users followed by target_user's following
        recommends = self.followed_by(target_user) + self.followings_followed(
            target_user
        )
        # Then we recommend some 'other' users
        recommends = recommends + [
            last
            for last in self.lr2dr(
                self.transitive(self.symmetric(self.dr2lr(self.relationship)))
            ).get(target_user, [])
            if last not in recommends
        ]
        # Last we remove target_user itself and those who alraedy in following
        return [
            user
            for user in recommends
            if (user != target_user and user not in self.followings_of(target_user))
        ]

    def dr2lr(self, dr):
        # This turn a constructive Dict Relationship
        # into a peer-to-peer List Relationship
        return [
            (user, following)
            for user, followings in dr.items()
            for following in followings
        ]

    def lr2dr(self, lr):
        # Vice versa
        return {
            user: [follower for left, follower in lr if left == user]
            for user in {left for left, _ in lr}
        }

    def symmetric(self, lr):
        return lr + [(y, x) for x, y in lr if (y, x) not in lr]

    def transitive(self, lr):
        # Sort for consistent indexing
        nodes = sorted({i for i, j in lr} | {j for i, j in lr})
        # Create adjacency matrix
        matrix = [[True if (x, y) in lr else False for y in nodes] for x in nodes]

        # Warshall Algorithm
        n = len(nodes)
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    matrix[i][j] = matrix[i][j] or (matrix[i][k] and matrix[k][j])

        return [
            (nodes[i], nodes[j]) for i in range(n) for j in range(n) if matrix[i][j]
        ]

    def generate_circles(self, users):
        """
        Generate social circles (i.e., equivalence classes) using binary relation properties:
        symmetric and transitive closures.
    
        Parameters:
        rel: An instance of Relationship that contains follow relationships.
        users: List of all usernames.
        
        Returns:
        circles: A list of sets, where each set represents a social circle (an equivalence class).
        """
        # Convert the relationship dictionary into a binary relation (list of (user, followed) pairs)
        lr = self.dr2lr(self.relationship)
        # Compute the symmetric closure: if (A, B) is in the relation, ensure (B, A) is also included.
        sym_lr = self.symmetric(lr)
        # Compute the transitive closure (using Warshall's algorithm) of the symmetric relation.
        trans_lr = self.transitive(sym_lr)
        # Convert the transitive closure (list of pairs) back into a dictionary mapping:
        # each key maps to the list of users in the same equivalence class.
        eq_dict = self.lr2dr(trans_lr)

        circles = []
        for user in users:
            # For each user, its equivalence class is the set of users related to it (if available)
            # plus the user itself.
            if user in eq_dict:
                group = set(eq_dict[user])
                group.add(user)
            else:
                group = {user}  # Isolated user forms a singleton circle.

            # Add the group to circles if it is not already included.
            if not any(group == existing for existing in circles):
                circles.append(group)
        
        # Sort circles by the smallest member (alphabetically) for consistent output.
        circles.sort(key=lambda s: sorted(s)[0])
        return circles

def test():
    rel = Relationship()
    rel.follow("A", ["B"])
    rel.follow("B", ["E", "I"])
    rel.follow("C", ["D", "H"])
    rel.follow("D", ["C"])
    rel.follow("E", [])
    rel.follow("F", [])
    rel.follow("G", ["E"])
    rel.follow("H", [])
    rel.follow("I", [])
    rel.follow("J", ["A"])
    print(rel.recommend("A"))
    print(rel.recommend("B"))
    print(rel.recommend("C"))

if __name__ == "__main__":
    test()