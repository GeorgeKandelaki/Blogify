

from ext import app

from routes import (
    renderLogin,
    renderSignup,
    renderOverview,
    renderUser,
    changeCurrentUsersPassword,
    updateCurrentUser,
    renderOwnedBlogs,
    renderBlog,
    renderBlogForm,
    renderEditPage,
    deleteBlog,
    renderSearchedBlogs,
    upvote_blog,
    downvote_blog,
    create_comment,
    delete_comment,
    edit_comment,
    upvote_comment,
    downvote_comment,
    logoutUser,
    deleteUser,
)

app.run(debug=True, host="0.0.0.0")
