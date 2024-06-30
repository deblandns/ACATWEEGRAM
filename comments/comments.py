# a simple function that give random not repetitive comment
import random

comments = [
    '👏 Appreciate the detailed report !',
    '📢 Great coverage of the topic !',
    '🌟 This article was very insightful !',
    '👍 Thanks for sharing the news !',
    '📰 Interesting update on current events !'
]

used_comments = []


def random_comment() -> str:
    global comments, used_comments

    # this will Reset the comments list if all have been used
    if len(comments) == 0:
        comments = used_comments[:]
        used_comments = []

    # this variable will Pick a random comment
    comment_picked = random.choice(comments)

    # this section will remove the picked comment from the comments list and add it to the used comments list
    comments.remove(comment_picked)
    used_comments.append(comment_picked)

    return comment_picked


# Example usage
for _ in range(1):  # To see the effect over multiple iterations
    print(random_comment())
