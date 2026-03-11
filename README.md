# 📌 SVG Project Card API

Welcome to **SVG Projects Card** – an elegant API that queries GitHub repositories and generates beautiful SVG visualizations. These SVGs can be embedded in GitHub READMEs or websites.

## 🚀 Features

- **Integration with GitHub README.md** – Generate SVG project cards and embed them in your profile.
- **Integration with HTML pages** – Retrieve all, selected, or pinned repositories as a JSON object with SVG cards.
- **Themes & Customization** – Choose from four themes: `dark | light | warm | cool`.

---

## 📖 Table of Contents

- [Getting All Repositories](#getting-all-repositories)
- [Getting a Single Repository](#getting-a-single-repository)
- [GitHub Integration](#github-integration)

---

## 🔍 Getting All Repositories

You can query the endpoint below to retrieve multiple repositories with custom SVG cards.

- To get **only pinned repositories**, use `pinned=True`.
- To get **all public repositories**, use `pinned=False`.
- To select a **theme**, use one of: `dark | light | warm | cool`.

### 📝 **Request Example**

```sh
GET https://svg-projects-card.onrender.com/api/username/repos?theme=dark&pinned=True
```

### 📩 **Response Example 200**

```json
{
  "status": true,
  "message": "Repositories retrived successfully.",
  "data": [
    { "svg": "<svg>...</svg>", "project_url": "project_git_url" },
    { "svg": "<svg>...</svg>", "project_url": "project_git_url" },
    { "svg": "<svg>...</svg>", "project_url": "project_git_url" }
  ]
}
```

### You can also use the API on your page like this:

```html
<body>
  <main>
    <div
      class="container"
      style="display: flex; gap: 1rem; flex-wrap: wrap"
    ></div>
  </main>
  <script>
    fetch(
      "https://svg-projects-card.onrender.com/api/BulusHamnu/repos?theme=dark&pinned=true",
    )
      .then((res) => res.json())
      .then((data) => {
        const container = document.querySelector(".container");

        data.data.forEach((repo) => {
          const card = document.createElement("div");
          card.innerHTML = repo.svg;
          card.onclick = () => {
            window.location.href = repo.project_url;
          };
          container.appendChild(card);
        });
      })
      .catch((err) => console.error(err));
  </script>
</body>
```

This fetches the repositories from the API and inserts the returned SVG cards into the page dynamically.

### 🖼️ **Adding Cover Images**

To add a **cover image**, use a `POST` request (since `GET` does not support `imageurl` when quering multiple repository).

#### **POST Request Example**

```sh
POST https://svg-projects-card.onrender.com/api/username/repos
```

#### **Request Body (JSON Format)**

```json
{
  "status": true,
  "message": "Repos retrived successfully.",
  "repos": [
    {
      "name": "animeq-game",
      "theme": "cool",
      "imageurl": "https://bulusdev.vercel.app/Assets/images/animequiz.png"
    },
    {
      "name": "Portfolio-V1",
      "theme": "light",
      "imageurl": "https://bulusdev.vercel.app/Assets/images/bulus_dev_cover.png"
    },
    {
      "name": "Demi-Tasks",
      "theme": "warm",
      "imageurl": "https://bulusdev.vercel.app/Assets/images/demi_tasks_cover.png"
    }
  ]
}
```

#### **JavaScript Fetch Example**

```js
fetch("https://svg-projects-card.onrender.com/api/BulusHamnu/repos", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    repos: [
      {
        name: "animeq-game",
        theme: "cool",
        imageurl: "https://bulusdev.vercel.app/Assets/images/animequiz.png",
      },
      {
        name: "Portfolio-V1",
        theme: "light",
        imageurl:
          "https://bulusdev.vercel.app/Assets/images/bulus_dev_cover.png",
      },
      {
        name: "Demi-Tasks",
        theme: "warm",
        imageurl:
          "https://bulusdev.vercel.app/Assets/images/demi_tasks_cover.png",
      },
    ],
  }),
});
```

### 📩 **Response Example**

```json
{
  "status": true,
  "message": "Repositories retrived successfully.",
  "data": [
    { "svg": "<svg>...</svg>", "project_url": "project_git_url" },
    { "svg": "<svg>...</svg>", "project_url": "project_git_url" },
    { "svg": "<svg>...</svg>", "project_url": "project_git_url" }
  ]
}
```

---

## 🎯 Getting a Single Repository

This is one of the best parts of the API. You can simply use an `img` tag and set the `src` to a link like this:

### Example

```html
<img
  src="https://svg-projects-card.onrender.com/api/username/repos/Demi-Tasks?theme=dark"
  alt="Project Card"
/>
```

Result:

<img src="https://svg-projects-card.onrender.com/api/bulushamnu/repos/Demi-Tasks?theme=light" alt="Demi-Tasks">

Because the API returns the response as an `image/svg`, the browser automatically renders it as an image.

**Note:** You can customize the card using the following query parameters:

- **theme** → `dark | light | warm | cool`
- **imageurl (optional)** → Add a cover image (must be a valid URL).

To retrieve a **single repository's SVG card**, use this format:

---

### 🎨 **Embedding in Markdown**

```markdown
![Demi-Tasks](https://svg-projects-card.onrender.com/api/username/repos/Demi-Tasks?theme=dark)
```

### **Preview of the Response**

![readme-svg-projects-card](https://svg-projects-card.onrender.com/api/BulusHamnu/repos/readme-svg-projects-card?theme=dark)

---

## 🛠️ GitHub Integration

This API enhances your **GitHub README.md** by embedding stylish project cards.

### 📝 **Embedding a Single Project**

```markdown
![Project Visualization](https://svg-projects-card.onrender.com/api/BulusHamnu/repos/Demi-Tasks?theme=dark)
```

or

```html
<img
  src="https://svg-projects-card.onrender.com/api/BulusHamnu/repos/Portfolio-V1?theme=dark"
  alt="Portfolio-V1"
/>
```

### 📌 **Displaying Multiple Projects in a README**

Well i am still working on that

---

**I built this project when I started learning backend development with Flask. If you like the project, consider giving it a star on GitHub!**
