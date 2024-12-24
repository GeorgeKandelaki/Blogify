from models import Comment_Down_Votes, Comment_Up_Votes, Up_votes, Down_votes

from sqlalchemy import and_


def findById(arr, id):
    for el in arr:
        if el.id == id:
            return el

    return False


def get_votes(user_id, comment_id):
    upvote = Comment_Up_Votes.query.filter(
        and_(Comment_Up_Votes.comment == comment_id, Comment_Up_Votes.user == user_id)
    ).first()

    downvote = Comment_Down_Votes.query.filter(
        and_(
            Comment_Down_Votes.comment == comment_id, Comment_Down_Votes.user == user_id
        )
    ).first()

    return [upvote, downvote]


def get_votes_blogs(user_id, blog_id):
    upvote = Up_votes.query.filter(
        and_(Up_votes.blog == blog_id, Up_votes.user == user_id)
    ).first()

    downvote = Down_votes.query.filter(
        and_(Down_votes.blog == blog_id, Down_votes.user == user_id)
    ).first()

    return [upvote, downvote]
