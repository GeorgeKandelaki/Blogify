from ext import app, db
from models import (
    Blog,
    User,
    Comment,
    Up_votes,
    Down_votes,
    Comment_Down_Votes,
    Comment_Up_Votes,
)


blogs = [
    {
        "name": "Understanding Artificial Intelligence",
        "description": "Exploring the basics of AI and its applications.",
        "article": "Artificial intelligence (AI) is a branch of computer science that focuses on building smart machines capable of performing tasks that typically require human intelligence. AI is used in a wide range of applications, from self-driving cars to personalized recommendations on streaming platforms. Understanding AI involves exploring machine learning, natural language processing, and neural networks. It is a transformative technology shaping our world in unprecedented ways.",
        "user": 1,
        "likes": 120,
        "dislikes": 5,
    },
    {
        "name": "The Secrets of Healthy Living",
        "description": "A guide to maintaining a healthy lifestyle.",
        "article": "Living a healthy life is not just about diet and exercise; it involves a holistic approach that includes mental well-being, good sleep habits, and regular physical activity. Eating a balanced diet rich in fruits, vegetables, and lean proteins fuels the body, while mindfulness and meditation nurture the mind. Incorporating small changes like walking more, drinking water, and getting quality sleep can significantly impact your health.",
        "user": 2,
        "likes": 98,
        "dislikes": 7,
    },
    {
        "name": "Mastering JavaScript in 2024",
        "description": "A complete guide to modern JavaScript.",
        "article": "JavaScript continues to be a cornerstone of web development. In 2024, the language is more versatile than ever, with frameworks like React, Angular, and Vue.js shaping user experiences. Mastering JavaScript involves understanding concepts such as closures, promises, and async/await. Developers must also grasp ES6+ features like destructuring, template literals, and arrow functions to stay ahead in the rapidly evolving tech landscape.",
        "user": 3,
        "likes": 210,
        "dislikes": 10,
    },
    {
        "name": "Blockchain: Beyond Cryptocurrency",
        "description": "Exploring non-financial uses of blockchain technology.",
        "article": "Blockchain is often associated with cryptocurrencies like Bitcoin, but its applications go far beyond digital money. From supply chain management to secure voting systems, blockchain provides transparency and immutability, making it invaluable in numerous industries. Companies are now leveraging blockchain for data security, identity verification, and even healthcare record management.",
        "user": 4,
        "likes": 150,
        "dislikes": 8,
    },
    {
        "name": "The Power of Mindfulness",
        "description": "How mindfulness can transform your life.",
        "article": "Mindfulness is the practice of being fully present in the moment. It has been scientifically proven to reduce stress, improve focus, and enhance overall well-being. Mindfulness can be cultivated through meditation, deep breathing, and even daily activities like eating or walking. The key is to engage fully with the present moment, letting go of distractions and negative thoughts.",
        "user": 5,
        "likes": 170,
        "dislikes": 4,
    },
    {
        "name": "The Future of Space Exploration",
        "description": "What lies ahead in humanity's journey into space.",
        "article": "Space exploration is entering a new era with advancements in technology and international collaborations. Mars colonization, asteroid mining, and deep-space exploration are becoming increasingly plausible. Companies like SpaceX and Blue Origin are revolutionizing space travel, while governments invest in ambitious projects like the Artemis program, aiming to establish a sustainable human presence on the Moon.",
        "user": 6,
        "likes": 200,
        "dislikes": 6,
    },
    {
        "name": "The Benefits of Renewable Energy",
        "description": "Why renewable energy is the future.",
        "article": "Renewable energy sources such as solar, wind, and hydroelectric power are becoming essential in combating climate change. These sustainable energy solutions reduce greenhouse gas emissions and dependence on fossil fuels. Innovations in energy storage and grid technologies are making renewables more efficient and accessible, paving the way for a cleaner, greener future.",
        "user": 7,
        "likes": 130,
        "dislikes": 9,
    },
    {
        "name": "The Psychology of Success",
        "description": "Uncovering the mindset behind achievement.",
        "article": "Success is not merely a result of talent or luck; it is deeply rooted in one's mindset. A growth mindset, resilience, and the ability to embrace failure as a learning opportunity are critical components. Cultivating habits like setting clear goals, staying disciplined, and maintaining a positive outlook can significantly influence one's journey toward success.",
        "user": 8,
        "likes": 250,
        "dislikes": 12,
    },
    {
        "name": "Exploring the Deep Ocean",
        "description": "The mysteries of the deep sea.",
        "article": "The deep ocean is one of the least explored frontiers on Earth, harboring incredible biodiversity and geological wonders. Advances in submersible technology and remote-operated vehicles (ROVs) have enabled scientists to study deep-sea ecosystems, from hydrothermal vents to bioluminescent creatures. This research not only enriches our understanding of marine life but also uncovers resources that could benefit humanity.",
        "user": 9,
        "likes": 160,
        "dislikes": 3,
    },
    {
        "name": "The Art of Storytelling",
        "description": "Why storytelling is a timeless skill.",
        "article": "Storytelling is a universal form of communication that connects people and conveys ideas in a compelling way. From ancient oral traditions to modern digital media, stories have the power to educate, entertain, and inspire. Mastering storytelling involves understanding your audience, crafting a clear message, and using emotion and authenticity to make your narrative resonate.",
        "user": 10,
        "likes": 190,
        "dislikes": 2,
    },
    {
        "name": "The Evolution of Modern Medicine",
        "description": "How medicine has transformed through centuries.",
        "article": "From herbal remedies to advanced gene therapy, medicine has evolved dramatically over centuries. Innovations like vaccines, antibiotics, and surgical techniques have revolutionized healthcare. The modern era now focuses on personalized medicine, leveraging genetic data to provide targeted treatments that enhance outcomes and reduce side effects.",
        "user": 11,
        "likes": 210,
        "dislikes": 4,
    },
    {
        "name": "The Influence of Social Media",
        "description": "Analyzing the impact of social media on society.",
        "article": "Social media has transformed how we communicate, share information, and shape opinions. While it offers opportunities for connection and expression, it also poses challenges like misinformation and mental health impacts. Understanding its influence requires a balance between embracing its benefits and addressing its pitfalls.",
        "user": 12,
        "likes": 140,
        "dislikes": 6,
    },
    {
        "name": "The Importance of Clean Code",
        "description": "How writing clean code can improve development productivity.",
        "article": "Clean code is more than just aesthetically pleasing; it’s a critical component of software maintainability. Writing clean code involves using meaningful variable names, maintaining proper indentation, and structuring your code into reusable functions or modules. For instance, instead of having long functions that perform multiple tasks, breaking them into smaller, single-purpose functions makes debugging and collaboration easier. Clean code also incorporates clear documentation and comments to help future developers (or even yourself) understand the code's intent. This article explores practical strategies to write cleaner, more readable code, such as adhering to coding standards, avoiding hardcoding values, and using consistent naming conventions. In the long run, clean code saves time, reduces technical debt, and ensures higher software quality.",
        "user": 1,
        "likes": 80,
        "dislikes": 3,
    },
    {
        "name": "An Introduction to TypeScript",
        "description": "Why TypeScript is becoming a developer favorite for large-scale projects.",
        "article": "TypeScript is a strongly typed superset of JavaScript that compiles down to plain JavaScript. It brings static typing to JavaScript, making your code more predictable and easier to debug. One of the key benefits of TypeScript is its ability to catch type-related errors during compile time, saving hours of runtime debugging. This article explores the basics of TypeScript, from defining types and interfaces to utilizing advanced features like generics and decorators. We also examine how TypeScript integrates seamlessly with modern frameworks like Angular and React, providing robust tooling and auto-completion. If you're working on a large-scale project or collaborating in a team, TypeScript can significantly enhance productivity and maintainability.",
        "user": 2,
        "likes": 110,
        "dislikes": 6,
    },
    {
        "name": "Exploring RESTful APIs with Flask",
        "description": "A beginner-friendly guide to creating APIs with Flask.",
        "article": "RESTful APIs have become the backbone of modern web applications, enabling seamless communication between the front-end and back-end. Flask, a lightweight Python framework, simplifies the process of building these APIs. In this article, we start with setting up Flask and creating basic routes. You'll learn how to handle HTTP methods like GET, POST, PUT, and DELETE, enabling CRUD operations for your application. We'll also explore integrating Flask with SQLAlchemy for database management and using Flask-RESTful to enhance API development. By the end, you'll have a solid understanding of how to build secure and efficient APIs that can power web and mobile applications.",
        "user": 3,
        "likes": 130,
        "dislikes": 4,
    },
    {
        "name": "Getting Started with Git and GitHub",
        "description": "A step-by-step guide to version control and collaboration.",
        "article": "Git and GitHub are indispensable tools for modern developers, enabling version control and collaboration. This guide starts with the basics of Git, explaining concepts like repositories, commits, and branches. You’ll learn how to initialize a Git repository, track changes, and commit code. Once comfortable with Git, the guide transitions to GitHub, covering how to create repositories, push code, and manage pull requests. Additionally, we explore advanced workflows like rebasing, resolving merge conflicts, and implementing continuous integration pipelines. By mastering Git and GitHub, you'll not only streamline your development process but also open up opportunities to collaborate effectively with developers worldwide.",
        "user": 4,
        "likes": 145,
        "dislikes": 8,
    },
    {
        "name": "The Rise of Serverless Architecture",
        "description": "Why serverless computing is gaining traction among developers.",
        "article": "Serverless architecture is revolutionizing how applications are built and deployed. By abstracting the underlying infrastructure, developers can focus solely on writing code while the cloud provider handles scaling, patching, and maintenance. This article discusses the core concepts of serverless computing, including Function-as-a-Service (FaaS) platforms like AWS Lambda, Azure Functions, and Google Cloud Functions. We’ll explore real-world use cases such as event-driven workflows, real-time data processing, and backend APIs. The article also highlights the pros and cons of serverless, including reduced operational complexity versus potential cold-start latency. Serverless architecture is paving the way for faster, more cost-effective development, making it a must-know for developers in 2024.",
        "user": 5,
        "likes": 160,
        "dislikes": 12,
    },
    {
        "name": "Demystifying JavaScript Closures",
        "description": "A deep dive into one of JavaScript’s most powerful features.",
        "article": "Closures are a fundamental yet often misunderstood feature of JavaScript. At its core, a closure is the combination of a function and its lexical environment, allowing the function to access variables from its outer scope even after the outer function has executed. This article explains closures with real-world examples, such as maintaining state in a counter function or encapsulating private variables in a module. We also cover advanced use cases, like partial function application and function factories. By understanding closures, you'll unlock new ways to write more efficient, modular, and reusable JavaScript code, elevating your skills as a developer.",
        "user": 6,
        "likes": 105,
        "dislikes": 7,
    },
    {
        "name": "Building Responsive Designs with SCSS",
        "description": "How SCSS makes it easier to create adaptive layouts.",
        "article": "SCSS, a popular preprocessor for CSS, simplifies the process of creating responsive designs. With features like variables, mixins, and nesting, SCSS streamlines the development of adaptive layouts for multiple screen sizes. This article explores practical techniques such as using mixins for media queries and employing variables for consistent spacing and breakpoints. We’ll also discuss how SCSS can organize large stylesheets into manageable partials, making your codebase cleaner and more maintainable. Whether you're building a single-page portfolio or a complex web application, SCSS offers the flexibility and efficiency needed for modern, responsive web design.",
        "user": 7,
        "likes": 98,
        "dislikes": 5,
    },
    {
        "name": "Introduction to Docker for Developers",
        "description": "How Docker simplifies application development and deployment.",
        "article": "Docker has become a cornerstone technology for modern application development. It allows developers to package applications and their dependencies into portable containers that run consistently across environments. This article starts with the basics, explaining what containers are and how they differ from virtual machines. We then move on to creating a simple Dockerfile, building an image, and running a container. Advanced topics like Docker Compose for multi-container setups and integrating Docker with CI/CD pipelines are also covered. By mastering Docker, you'll simplify development workflows, eliminate 'works on my machine' problems, and streamline deployment processes.",
        "user": 8,
        "likes": 140,
        "dislikes": 6,
    },
    {
        "name": "Optimizing Web Performance",
        "description": "Techniques for faster load times and smoother user experiences.",
        "article": "Web performance is critical for user retention and SEO. This article explores strategies to optimize web applications, including minifying CSS and JavaScript files, optimizing images, and using lazy loading for non-critical resources. We also delve into server-side techniques like caching, using Content Delivery Networks (CDNs), and leveraging HTTP/2 for faster data transfer. Additionally, tools like Lighthouse and WebPageTest are discussed to measure and improve performance metrics such as Time to First Byte (TTFB) and Largest Contentful Paint (LCP). By implementing these techniques, you can ensure your website not only looks good but also delivers a fast, seamless user experience.",
        "user": 9,
        "likes": 125,
        "dislikes": 9,
    },
    {
        "name": "Securing Your Web Application",
        "description": "Best practices to safeguard your app against common vulnerabilities.",
        "article": "With cyber threats on the rise, securing your web application is more important than ever. This article covers essential practices like implementing HTTPS, validating user input to prevent SQL injection and cross-site scripting (XSS), and securing authentication with techniques like hashing passwords using bcrypt. We also discuss advanced topics like Content Security Policy (CSP) and monitoring application activity for suspicious behavior. By the end of this guide, you'll have a clear roadmap for securing your web applications, protecting user data, and staying ahead of potential vulnerabilities in an ever-evolving threat landscape.",
        "user": 10,
        "likes": 185,
        "dislikes": 15,
    },
    {
        "name": "The Role of Artificial Intelligence in Education",
        "description": "How AI is transforming learning environments.",
        "article": "Artificial intelligence is revolutionizing the education sector by personalizing learning experiences, automating administrative tasks, and providing new tools for educators. With AI, students can access adaptive learning platforms that cater to their unique needs, while teachers can gain insights from data analytics to improve instruction.",
        "user": 13,
        "likes": 300,
        "dislikes": 10,
    },
    {
        "name": "Cybersecurity in the Digital Age",
        "description": "Staying safe in a connected world.",
        "article": "As technology becomes more integrated into daily life, cybersecurity is increasingly vital. Protecting personal and professional data from cyber threats requires awareness, best practices, and robust security systems. Understanding concepts like phishing, encryption, and secure browsing can help individuals and organizations stay protected.",
        "user": 14,
        "likes": 120,
        "dislikes": 5,
    },
    {
        "name": "Sustainable Architecture and Design",
        "description": "Building a greener future.",
        "article": "Sustainable architecture prioritizes eco-friendly practices in construction and design. From energy-efficient buildings to the use of renewable materials, this approach minimizes environmental impact while creating functional spaces. Architects are increasingly incorporating green roofs, solar panels, and natural ventilation to enhance sustainability.",
        "user": 15,
        "likes": 150,
        "dislikes": 4,
    },
    {
        "name": "Top 10 ChatGPT prompts to learn anything 10 times faster",
        "description": "Copy & paste these ChatGPT prompts to learn anything 10X faster  Quickly gain & retain knowledge! Save valuable time.",
        "article": """ 
Use these top 10 ChatGPT prompts:

Prompt 1 - Complex Topic Decoder

Break down [Difficult Subject] into 5 core principles. Use real-world metaphors for each. Create mini-challenges to test understanding. Build a 7-day mastery path with quick-win milestones. Include a “clarity score” after each mini-test.

My learning goal: [Learning Goal].

Prompt 2 - Learning Acceleration Blueprint

Design a 21-day rapid learning system for [Topic]. Structure into morning theory, afternoon practice, and evening review. Create dopamine-triggering rewards for each milestone. Include focus-state triggers and retention measurements.

My available time: [Study Time].

Prompt 3 - Knowledge Web Builder

Transform [Topic] into an interconnected concept map. Create memory hooks linking new information to existing knowledge. Design a 5-minute daily review system. Include understanding depth score. Generate quick recall patterns.

My current knowledge: [Current Level].

Prompt 4 - Book Mastery System

Extract core principles from [Book]. Create an action-focused summary with implementation steps. Design a 30-day practice plan for key concepts. Include knowledge application score. Generate real-world testing scenarios.

My learning focus: [Book Topic].

Prompt 5 - Problem-Solving Framework

Build a rapid solution system for [Subject] challenges. Create decision trees for common problems. Include quick-check validation methods—design difficulty progression path. Generate solution speed metrics.

My skill level: [Current Level].

Prompt 6 - Case Study Analyzer

Create a framework to extract insights from [Topic] cases. Build a pattern recognition system. Design implementation roadmap for lessons learned. Include practical application scores. Generate quick-action templates.

My analysis goal: [Analysis Goal].

Prompt 7 - Writing Enhancement System

Develop a daily writing improvement plan for [Style/Purpose]. Create templates for common scenarios. Include style consistency checks. Design reader impact measurements. Generate progress tracking metrics.

My writing goal: [Writing Goal].

Prompt 8 - Interview Success Accelerator

Build a rapid preparation system for [Interview Type]. Create answer frameworks with impact stories. Design confidence-building exercises. Include presence measurement score. Generate quick recovery tactics.

My interview goal: [Interview Goal].

Prompt 9 - Language Learning Optimizer

Design an immersive learning environment for [Language]. Create daily conversation scenarios. Build pronunciation improvement systems. Include fluency progress metrics. Generate quick practice routines.

My language goal: [Language Goal].

Prompt 10 - Hobby Mastery Roadmap

Create structured learning paths for [Hobby]. Break into daily skill-building exercises. Design progress validation system. Include enjoyment-to-effort ratio. Generate skill demonstration opportunities.

My target level: [Desired Level].

""",
        "likes": 300,
        "dislikes": 10,
        "user": 16,
    },
]

users = [
    {
        "name": "Admin",
        "email": "admin@blogify.com",
        "password": "giogio2008",
        "image": "default.jpg",
        "role": "admin",
    },
    {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "password": "giogio2008",
        "image": "default.jpg",
        "role": "user",
    },
    {
        "name": "Jane Smith",
        "email": "janesmith@example.com",
        "password": "giogio2008",
        "image": "default.jpg",
        "role": "user",
    },
    {
        "name": "Robert Johnson",
        "email": "robertjohnson@example.com",
        "password": "giogio2008",
        "image": "default.jpg",
        "role": "user",
    },
    {
        "name": "Emily Davis",
        "email": "emilydavis@example.com",
        "password": "giogio2008",
        "image": "default.jpg",
        "role": "user",
    },
    {
        "name": "Michael Brown",
        "email": "michaelbrown@example.com",
        "password": "giogio2008",
        "image": "default.jpg",
        "role": "user",
    },
    {
        "name": "Sarah Miller",
        "email": "sarahmiller@example.com",
        "password": "giogio2008",
        "image": "default.jpg",
        "role": "user",
    },
    {
        "name": "David Wilson",
        "email": "davidwilson@example.com",
        "password": "giogio2008",
        "image": "default.jpg",
        "role": "user",
    },
    {
        "name": "Jessica Moore",
        "email": "jessicamoore@example.com",
        "password": "giogio2008",
        "image": "default.jpg",
        "role": "user",
    },
    {
        "name": "Daniel Taylor",
        "email": "danieltaylor@example.com",
        "password": "giogio2008",
        "image": "default.jpg",
        "role": "user",
    },
    {
        "name": "Sophia Anderson",
        "email": "sophiaanderson@example.com",
        "password": "giogio2008",
        "image": "default.jpg",
        "role": "user",
    },
    {
        "name": "Matthew Thomas",
        "email": "matthewthomas@example.com",
        "password": "giogio2008",
        "image": "default.jpg",
        "role": "user",
    },
    {
        "name": "Olivia Lee",
        "email": "olivialee@example.com",
        "password": "giogio2008",
        "image": "default.jpg",
        "role": "user",
    },
    {
        "name": "James Harris",
        "email": "jamesharris@example.com",
        "password": "giogio2008",
        "image": "default.jpg",
        "role": "user",
    },
    {
        "name": "Isabella Clark",
        "email": "isabellaclark@example.com",
        "password": "giogio2008",
        "image": "default.jpg",
        "role": "user",
    },
    {
        "name": "Alexander Walker",
        "email": "alexanderwalker@example.com",
        "password": "giogio2008",
        "image": "default.jpg",
        "role": "user",
    },
]


with app.app_context():
    db.drop_all()
    db.create_all()

    for blog in blogs:
        b = Blog(
            name=blog["name"],
            description=blog["description"],
            article=blog["article"],
            user=blog["user"],
            likes=blog["likes"],
            dislikes=blog["dislikes"],
        )
        Blog.add(b)

    db.session.commit()

    for user in users:
        u = User(
            name=user["name"],
            email=user["email"],
            password=user["password"],
            image=user["image"],
            role=user["role"],
        )
        User.add(u)

    db.session.commit()
