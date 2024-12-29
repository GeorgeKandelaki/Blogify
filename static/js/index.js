"use strict";

const editForm = document.querySelector(".form__edit-blog");
const blogOptions = document.querySelector(".blog__options");
const commentOptions = document.querySelector(".comments");
const blogWrapper = document.querySelector(".blog__wrapper");
const blogs = document.querySelector(".blogs");

if (editForm) {
	const article = editForm.querySelector(".blog__article-field");
	const {
		dataset: { x },
	} = article;

	article.innerHTML = x;
}

if (blogOptions) {
	document.body.addEventListener("click", (e) => {
		const { target } = e;

		if (target.matches(".blog__options-icon")) blogOptions.classList.toggle("content--disable");

		return;
	});
}

if (commentOptions) {
	document.body.addEventListener("click", (e) => {
		const { target } = e;

		if (target.matches(".comment__options-icon")) {
			target.parentElement.nextElementSibling.classList.toggle("content--disable");
			return;
		}

		if (target.matches(".comment__edit")) {
			const comment = target.closest(".comment");
			const input = comment.querySelector(".comment__edit-input");
			const {
				dataset: { x: value },
			} = input;
			input.textContent = value;

			comment.querySelector(".comment__content").classList.toggle("content--disable");
			comment.querySelector(".comment__header").classList.toggle("content--disable");
			comment.querySelector(".comment__edit-form").classList.toggle("content--disable");
			comment.querySelector(".comment__interactions").classList.toggle("content--disable");

			return;
		}
	});
}

if (blogs) {
	blogs.addEventListener("click", (e) => {
		const { target } = e;

		if (
			target.matches(".blog-card__wrapper") ||
			target.matches(".blog-card__image") ||
			target.matches(".heading-tertiary") ||
			target.matches(".blog-card__description")
		) {
			const { id } = target.closest(".blog-card");
			console.log(123);
			location.assign(`/blogs/${id}`);
			return;
		}
	});
}
