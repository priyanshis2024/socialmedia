from fastapi import FastAPI
from router import user,post,comment
from fetch import fetch_all_user,fetch_all_post,fetch_all_comment, fetch_single_post_detail_with_respective_comment_by_thier_user
from fetch import fetch_post_with_respective_user,fetch_post_detail_with_their_all_comments,fetch_only_comment_on_post
from fetch import fetch_all_post_detail_with_comment_and_user
from fetch import fetch_all_post_created_by_user_along_with_comment
app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(fetch_all_user.router)
app.include_router(fetch_all_post.router)
app.include_router(fetch_all_comment.router)
app.include_router(fetch_post_with_respective_user.router)
app.include_router(fetch_only_comment_on_post.router)
app.include_router(fetch_post_detail_with_their_all_comments.router)
app.include_router(fetch_single_post_detail_with_respective_comment_by_thier_user.router)
app.include_router(fetch_all_post_detail_with_comment_and_user.router)
app.include_router(fetch_all_post_created_by_user_along_with_comment.router)

@app.get("/")
def root():
    return "Welcome to the Social media API Backend"