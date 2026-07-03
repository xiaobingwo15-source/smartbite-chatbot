# Artificial Intelligence - Assignment Specifications

## Overview

* **Aims:** Enable students to analyse and employ appropriate Artificial Intelligence (AI) techniques to design intelligent systems and solve problems. Enable students to use any relevant tools and technology, such as Python programming, to develop intelligent computer programs.
* **Learning Outcomes Assessed:**
    * **CLO 2:** Demonstrate AI techniques and strategies to solve a given problem (A3, PLO9).
    * **CLO 3:** Produce AI application using programming language or other relevant technology (P4, PLO3).
* **Outline of Problem:** This is a group assignment. All members from each group are required to critically evaluate the current technologies, and then propose a project for the selected AI topic, implement an AI solution to solve the problem in the proposed project using either Python or other relevant tools.

## Details

This assignment consists of **TWO (2)** parts that are related to each other. Each group is required to develop a program using **Python** or **any other relevant tools**. Kindly refer to Project Part 1 and Project Part 2 for more information.

* Form a group of **TWO (2)** to **THREE (3)** members. Each group has to complete and submit a **Documentation (Part 1)** and **Program / Prototype with source code (Part 2)**. Team leader has to compile and submit the deliverables before the due date.
* **SIX (6)** options of research areas are listed in the following section named TITLE. Each group should select **ONE (1)** option and is expected to produce ideas that originated from the respective group members, but not to take the work or an idea of someone else (including from the Web) and pass it off as your own. Besides, **NO GROUP is allowed to share the same idea**. In other words, each group must propose a unique title or solution.
* The basic requirements for each research area are available in the Titles section (see below). It is important to note that fulfilling those requirements might only be helping you to get an **Average** or **Good grade**. In order to achieve an **Excellent grade**, extra efforts are required such as learning new skills, introducing new ideas, implementing complex AI algorithms, demonstrating the ability to process big data, and/or producing excellent reports with a working prototype.

---

## Titles (Research Areas)

### 1. Machine Learning (Supervised)
* Identify a classification problem to be solved (e.g., predicting disease presence, credit approval, etc.).
* Perform a background study on the selected problem and the supervised learning methods to be used (e.g., ANN, SVM, KNN, etc.).
* Search for the respective dataset. You may download a public dataset online or perform your own data gathering if required.
* Perform data pre-processing and data representation to prepare the dataset for model training (e.g., handling missing values, normalization, and feature engineering).
* Each group member must provide a solution using a preferred classification method (e.g., ANN, SVM, KNN).
* Compare the results of different classification methods in terms of evaluation metrics such as accuracy, precision, recall, and F1 score.
* **Hints for datasets:**
    * [UCI Machine Learning Repository](https://archive.ics.uci.edu/datasets)
    * [Kaggle Datasets](https://www.kaggle.com/datasets)
    * [OpenML](https://www.openml.org/search?type=data&sort=runs&status=active)

### 2. Machine Learning (Unsupervised)
* Identify a clustering problem to be solved (e.g., customer segmentation, image segmentation, or anomaly detection).
* Perform a background study on the selected problem and the unsupervised learning methods to be used (e.g., K-means, MeanShift, DBSCAN, etc.).
* Search for the respective dataset. You may download a public dataset online or perform your own data gathering if required.
* Perform data pre-processing and data representation to prepare the dataset for clustering analysis (e.g., scaling, encoding, and dimensionality reduction).
* Each group member must provide a solution using a preferred clustering method (e.g., K-means, MeanShift, DBSCAN).
* Compare the results of different clustering methods based on evaluation metrics such as inertia, silhouette score, or other appropriate metrics.
* **Hints for datasets:** (Same as Supervised Learning hints)

### 3. Recommender System
* Identify a real-life scenario where a recommender system can be applied to suggest products, services, or content. Examples include:
    * Recommending products or brands for an e-commerce platform.
    * Suggesting movies or TV shows for a streaming service.
    * Proposing books or academic articles for a library system.
    * Offering tailored services for procurement activities in a business.
* Perform a background study on:
    * The selected problem/scenario.
    * The type of recommender system to be implemented.
    * The expected functionalities and benefits of the system for the chosen scenario.
* Each group member must provide a solution using a preferred recommender system (e.g., collaborative filtering, content-based, or hybrid).
* Test and evaluate your recommender system to assess its efficiency and accuracy. Use appropriate evaluation metrics, such as:
    * Precision, recall, or F1 score.
    * Mean Squared Error (MSE) or Root Mean Squared Error (RMSE) for predicted ratings.
    * User satisfaction through questionnaire.
* **Hints & Resources:**
    * [IBM Product Recommendation](https://github.com/IBM/product-recommendation-with-watson-ml)
    * [Creating a Simple Recommender System in Python using Pandas](https://stackabuse.com/creating-a-simple-recommender-system-in-python-using-pandas/)
    * [How did we build Book Recommender Systems in an hour](https://towardsdatascience.com/how-did-we-build-book-recommender-systems-in-an-hour-the-fundamentals-dfee054f978e)

### 4. Natural Language Processing (NLP)
* Identify a problem or task related to Natural Language Processing (NLP). Examples include:
    * **Sentiment Analysis:** Determining whether a piece of text (e.g., tweets, reviews) is positive, negative, or neutral.
    * **Text Classification:** Categorizing text into predefined categories (e.g., spam detection).
* Perform background study on the problem and method to be used:
    * The chosen NLP problem or task.
    * The significance and applications of solving this problem in real-world scenarios.
    * Common methods and techniques used for the task (e.g., Bag-of-Words, TF-IDF, word embeddings, transformers).
* Create a web crawler to crawl sample data from a forum/social media or to use the dataset from any reliable website.
* Preprocess the data to make it suitable for analysis. This may include:
    * Text cleaning (removing stop words, punctuation, or special characters).
    * Tokenization, stemming, and lemmatization.
    * Feature extraction (e.g., TF-IDF, word embeddings using Word2Vec or BERT).
* Each member is required to develop and implement a different solution for the task using a preferred NLP method. Examples include:
    * **Sentiment Analysis:** Use methods such as Naïve Bayes, Support Vector Machine (SVM), or transformer-based models like BERT or GPT.
    * **Text Classification:** Implement algorithms like Logistic Regression, Decision Trees, or deep learning models.
* Compare and evaluate the performance of different NLP models using appropriate metrics, such as Accuracy, Precision, Recall, and F1 Score for classification tasks.
* **Hints & Datasets:**
    * [Sentiment Analysis Data](https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html)
    * [Twitter Analytics](http://adilmoujahid.com/posts/2014/07/twitter-analytics/)
    * [Yelp Dataset](https://www.yelp.com/dataset)
    * [Stanford Sentiment Data](https://ai.stanford.edu/~amaas/data/sentiment/)

### 5. Chatbot Development
* Identify a real-life scenario where a chatbot can be utilized. Examples include:
    * Customer support chatbot for an e-commerce platform.
    * FAQ chatbot for a university or organization.
    * Personal assistant chatbot for scheduling and reminders.
* Perform a Background Study:
    * Research existing chatbot technologies and applications.
    * Explore the capabilities and limitations of chatbots built using machine learning or platforms like Pandorabots, Google Dialogflow, Rasa, or Botpress.
* Choose a Development Approach:
    * **Option 1:** Build the chatbot using machine learning techniques. This may involve training a Natural Language Processing (NLP) model for intent recognition and response generation.
    * **Option 2:** Develop the chatbot using a platform such as Google Dialogflow, Pandorabots, Rasa or similar tools.
* Define the Chatbot’s Functionalities:
    * Answering FAQs.
    * Conducting natural conversations.
    * Providing recommendations, booking services, or troubleshooting issues.
* Each member is required to develop and implement a different Chatbot.
    * **For ML-based development:** Collect a dataset for training and testing; preprocess the data; train an ML/DL model for intent classification and response generation.
    * **For platform-based development:** Use the platform’s GUI/APIs to configure intents, entities, and responses; integrate additional functionalities (e.g., external APIs).
* Test the Chatbot: evaluate and compare different chatbot performance based on accuracy of intent recognition, response relevancy and quality, and user satisfaction.
* Evaluate the Chatbot using metrics such as: F1 Score, Precision, and Recall for intent classification; BLEU or ROUGE scores for response generation; Usability and user satisfaction ratings.
* **Hints & Resources:**
    * [Pandorabots](https://www.pandorabots.com/)
    * [IBM Watson Chatbot](https://www.ibm.com/watson/how-to-build-a-chatbot/)
    * [Building a Chatbot on Kaggle](https://www.kaggle.com/code/melkmanszoon/building-a-chatbot)

### 6. Image Processing and Computer Vision
* Identify an image processing or computer vision problem to be solved. For example:
    * Text detection and Optical Character Recognition (OCR)
    * Object Detection and Classification
    * Pedestrian Detection and Human Action Recognition
    * Face Recognition
    * Image Segmentation
* Perform background study on the problem and method to be used. Explore the state-of-the-art methods and technologies used to address the problem (e.g., Convolutional Neural Networks (CNNs), YOLO, Mask R-CNN, etc.).
* Search for the respective dataset (download a public dataset or perform data gathering).
* Data pre-processing and representation such as:
    * Image resizing, normalization, and augmentation.
    * Label encoding for classification tasks.
    * Annotation for object detection or segmentation tasks.
* Each member is required to develop using different algorithms such as CNN, Machine Learning, YOLO, etc. Compare the results of different methods in terms of accuracy, precision, recalls, etc. You can also demo the development system in real-life scenario (optional).
* Based on the results, explain the performance of the chosen methods (e.g., compare the advantage, disadvantage, and characteristics of the methods).
* **Hints & Datasets:**
    * [MNIST Handwritten Digits](http://yann.lecun.com/exdb/mnist/)
    * [PASCAL VOC 2012](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html)
    * [CIFAR-10](https://www.kaggle.com/c/cifar-10)
    * [LFW Face Recognition](http://vis-www.cs.umass.edu/lfw/)

---

## General Guidelines & Policies

### Submission Deadlines
* **Submit Documentation and Prototype Source Code by 28 August 2026 (Week 11, Friday, before 12pm).**
* Please submit your work to Google Classroom. Late submission will be penalized. A demo session to present the prototype is required in week 12 to week 14.

### Contribution
This assignment consists of the following TWO (2) components:
1.  **Documentation (40%)**
2.  **Prototype development (60%)**
*(Please check Appendix 1 and Appendix 2 for the assessment criteria).*

### Academic Integrity and Plagiarism
* There must be **ORIGINALITY** in your work. Thus, do not copy or refer to other group(s). You may only work with your team member(s) to produce the solution of this assignment. You must not share with nor refer to any part of the assignment (including the code) of anyone else except your team member(s) and your tutor.
* Before submitting your assignment, please make sure that you have complied with TARUMT Plagiarism Policy. Any cheating, attempt to cheat, plagiarism, collusion and any other attempts to gain an unfair advantage in assessment will cause the students concerned to be penalized.
* Each student is required to fill up **Appendix A: “Plagiarism Statement Form”** attached in the documentation template.
* **IMPORTANT:** Students found to be dishonest are liable to disciplinary action.

### AI Use Guideline
In this course, AI is recognised as a collaborative learning tool. Students are encouraged to utilise AI tools (e.g., ChatGPT, Claude, MidJourney) to support activities such as brainstorming, coding, or refining written work. However, **all AI use must be explicitly disclosed**. Students are required to include an **AI Disclosure Statement (Appendix B)** with each submission, specifying the AI tools and prompts used, as well as the steps taken to verify the accuracy and relevance of the AI-generated content. Students remain fully responsible for the accuracy, logic, and integrity of their final work.

### Free-Rider Guideline
* Discuss and document individual expected roles and responsibilities at the start of the group project/assignment/activity. Encourage open communication to resolve minor misunderstandings promptly.
* Keep evidence of work completed (meeting notes, drafts or communication records).
* When a group member is perceived as free-riding, the matter shall first be discussed within the team where possible.
* If no resolution is reached, the concerned student(s) may submit a **Student Free-Rider Report Form (Appendix C)** in the documentation template to the Course Coordinator/Lecturer/Tutor attached with the relevant evidence(s).
* The Course Coordinator/Lecturer/Assessor shall review the report and facilitate a fair resolution, which may include: Individual performance review, Advisory feedback or academic counselling before escalating to the Programme Leader for the commencement of Investigation Procedure.

### Late Submission & Penalty
Late submission without valid reason will **NOT** be tolerated. For late submission, there will be a reduction of total marks:
* **Late 1 to 3 days** after deadline: Deduction of 10 marks
* **Late 4 to 7 days** after deadline: Deduction of 20 marks
* **Late more than 7 days** after deadline: Deduction of 100 marks
* In certain circumstances, a student may be allowed to submit the assignment late with valid reason. S/he must contact the tutor at least one week before the assignment is due. The tutor will evaluate whether the circumstance warrants submitting the assignment late, but no guarantee that the students will not be penalized. Failing to submit the reports and code will lead to failure of the coursework.

---

## Project Part 1: Documentation

* **Introduction:** Your task for this part of the assignment is to identify a problem for the selected AI topic, perform a literature review and propose your respective AI solution(s) that helps in solving the problem in the proposed project.
* **How to write documentation?** Refer to the “Documentation Template”.

## Project Part 2: Prototype Development

* **Introduction:** Your task for this assignment is to implement an AI solution using Python or any other relevant tools, perform testing and evaluation on the system and finally present the work to your tutor.
* **What to hand in?** Follow instruction in google classroom. EACH team member is required to present their own work, demonstrate the prototype and be ready for a Q&A session in Week 12-14 based on the arrangement.

---

## APPENDIX 1: Documentation Assessment Rubrics (40%)
*Final score = sum of scores / 100 * 40*

| Item (CLO 2) | Missing or Unacceptable (0-4) | Poor (5-9) | Accomplished (10-15) | Good (16-20) |
| :--- | :--- | :--- | :--- | :--- |
| **Introduction** | Background, problem statement, objectives, and significance are missing or unclear. No clear research gap identified. | Background, problem statement, objectives, and significance are present but vague or partially explained. Limited understanding of research gap. | Clear background, problem statement, objectives, and significance. Research gap identified and explained. | Comprehensive and well-written introduction. Research gap is clearly justified. Objectives and significance are fully aligned with the study. |
| **Related Work** | Previous studies are poorly described or copied from literature without paraphrasing. No evaluation or comparison of prior work. | Some description of previous studies with limited evaluation or comparison. Gaps are vaguely mentioned. | Previous studies are described, evaluated, and compared. Research gaps are identified and justified. | Excellent critical analysis and comparison of prior work. Clear identification of gaps and strong justification for the current study. |
| **Methodology** | System flow, dataset, algorithm, or evaluation metrics are missing, irrelevant, or poorly described. | Methodology is briefly described but lacks clarity or completeness. Algorithm and metrics explanation are weak. | Methodology is well-explained with clear system flow, dataset description, algorithm, and evaluation metrics. | Methodology is comprehensive, logical, and clearly presented. Dataset, algorithms, and metrics are justified and appropriate for the study. |
| **Results & Discussion** | Results are missing, unclear, or unrelated to the objectives. No interpretation or discussion provided. | Results are presented but partially unclear or incomplete. Minimal discussion or interpretation. | Results are clearly presented and aligned with objectives. Discussion interprets results and addresses implications. | Results are comprehensive, well-presented, and clearly interpreted. Strong discussion of implications and relevance to the objectives. |
| **Conclusion & References & Source** | Achievements, limitations, and future work are missing or unclear. References and dataset/tool sources missing or improperly cited. | Achievements are mentioned but limited; limitations and future work are vaguely addressed. References or sources provided but not in proper format or incomplete. | Achievements, limitations, and future work are described and explained. References are complete and properly cited in APA style; datasets and tools are acknowledged. | Achievements are clearly stated, limitations acknowledged, and future improvements thoughtfully proposed. References are comprehensive, properly formatted, and all datasets/tools fully cited. Strong academic rigor demonstrated. |

---

## APPENDIX 2: Prototype Assessment Rubrics (60%)
*Final score = sum of scores*

| Item (CLO 3) | Poor (0-4) | Accomplished (5-7) | Good (8-10) |
| :--- | :--- | :--- | :--- |
| **User interface / Output (10%)** | Poor or confusing design of UI or output, which provides inadequate information/outputs. Most of the information/outputs generated are less accurate. Layout of information is not organized. | Adequate information/outputs needed are generated. The information/output generated are accurate but some with errors. Layout of information is organized. | All the necessary information/outputs are generated. All or most of the information/outputs generated are accurate. Minor errors can be ignored. Layout of information is well-organized. |
| **Degree of completion (10%)** | Too much still remain to be done. Basic requirements are not fulfilled. The end product produces enormous errors, faults or incorrect results. | All required features present in the interface within the required scope, but some are simplified. Or one or two features are missing. The system is able to run with minor errors. | All required features present in the interface within or beyond the required scope. No bugs during demonstration. |
| **System implementation (10%)** | The end product is produced with different system design or approach, which is not related to the initial proposal. | The end product conforms to most of the system design, but some are different from the specification. | The end product fully conforms to the proposed system design. |
| **Presentation and on-the-spot coding (10%)** | The student is unclear about the work produced, sometimes not even knowing where to find the source code. | The student knows the code whereabouts, but sometimes may not be clear why the work was done in such a way. | The student is clear about every piece of the work done. |

*(Note for Programming below: Scale is 0-20)*

| Item (CLO 3) | Poor (0-8) | Accomplished (9-15) | Good (16-20) |
| :--- | :--- | :--- | :--- |
| **Programming (20%)** | The end product fails with many logic errors, many actions lacked exception handling. Solutions are over-simplified. Programming skill needs improvement. Minimal validations are provided. Business rules are not validated. | Major parts are logical, but some steps to complete a specific job may be tedious or unnecessarily complicated. Program algorithm demonstrates acceptable level of complexity. The student is qualified to be a programmer. Important and necessary validations are provided. | Correct and logical flow, exceptions are handled well. Demonstrates appropriate or high level of complex algorithms and programming skills. Thorough and thoughtful validations are provided. All important business rules are validated. |
