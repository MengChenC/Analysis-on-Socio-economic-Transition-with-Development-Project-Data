## __Analysis on Socio-economic Transition with Development Project Data__

### __1. Research Question__
In this mini-project, I tried to explore the transition in financial projects from Inter-American Development Bank (IDB), aiming to see if the overall project topics shift with the timeframe. And if so, how do they change? By identifying the shift, I might understand not only the change of the institution’s financing guideline but also the growth and development among the areas covered by IDB.

### __2. Literature Review__
The concept of development intrinsically indicates a specified state of growth or advancement, and the projects from development banks capture the process and transition in the society and economy. Even projects from the same domain across a long timestamp (a year or longer) may emphasize different points of view or leverage different approaches to implement the project targets. For example, charcoal might have been a perfect energy source in the mid-1900s, and facilitating underdeveloped countries to grab this technique was appropriate during the time. Nonetheless, it has been deprecated since the 21 century, and international banks do not consider it a reliable energy source anymore in their development projects. Hence, identifying the projects and their shift can illustrate a higher-level overview of the regional and subregional transition and development. 

Topic modeling can mine the information from each project and categorize the project into the topic with the highest probability. In previous studies, researchers leveraged topic modeling to identify market trends and cultural values of heritage products on eBay [[1]](#1), or distinguish political identities through social media data [[2]](#2), both of which relied on calculating the probability of corpus and words. However, in order to visit the topics among different periods, I needed to employ a dynamic topic model (DTM). Blei and Lafferty proposed this method in 2006, allowing people to analyze the evolution of topics of a collection of documents over time. Unlike Latent Dirichlet Allocation (LDA) in static topic modeling, the order of the documents plays a fundamental role in DTM [[3]](#3). Based on this prototype, scholars also developed other applications, such as measuring scholarly impact using changes in the thematic content of documents over time [[4]](#4) or synthesizing historical change [[5]](#5). Moreover, to obtain ﬁner-grained time resolutions in DTM, researchers proposed a continuous time dynamic topic model (cDTM) to model a continuous time-space [[6]](#6). Nonetheless, they have not taken on leveraging DTM to extract socio-economic development and transition with financing project data. Thus, this mini-project demonstrated the potential application in identifying development with DTM.
### __3. Data__
I used the financial project dataset collected from the previous mini-project. The dataset contains IDB’s approved development projects from 1993 to 2021 mid-October. I had scraped the columns including *Project Status, Country, Date, Project Name, Project Number, Sector, Subsector, Project Type, Social Impact Category, Loan Amount, Bank, URL, Description*, but in order to leverage topic modeling to examine the topics among the projects, I focused on Date (the date a project is approved), Sector (the development type of a project), and Description (a brief overview of a project). With the textual data in the Description column, I could employ dynamic topic modeling to allocate the topics and examine their change over time slices. The sector parameter covers fundamental to advanced socio-economic fields, such as agriculture, energy, science and technology, etc. Hence, the modeling process should locate in the same sector to have meaningful topics and comparisons.

### __4. Method__
I followed the method mentioned by Blei and Lafferty in 2006 to explore the topic shift over time [[3]](#3). Since this method divides corpus into time slices, allowing topic distributions to evolve from time slice to time slice, I am able to examine the textual data within each timeframe and compare their transformation. In order to fit the dynamic topic model, several adjustments played a role. First, I filtered out data with fewer than 10 words in the description (i.e. they do not have enough textual data to conduct the analysis). For recent projects, there is no date information since the Date is recorded after being approved. However, it is certain that those projects will be approved after mid-October (since the project list is based on date ordering), hence I assigned their date to be mid-October 2021. Then I created a “Year” column from the Date by only retrieving the year index. Time slice is an element for dynamic topic modeling, I decided to compare among 2000, 2010, 2020 and expected the decade gap could capture the topic changing in the projects. Besides aggregating data by year, I also aggregated it by sector since having all sectors as a whole will be too many topics, which prevented the model from identifying the transition between different timestamps.

I then selected some sectors if they had enough data and were more relevant to socio-economic development, as well as with my interest: energy, environment, science and technology, social investment, and transportation. Besides filtering out the common stop words, I also removed some common terms (such as 'support', 'project', 'develop', etc.) in this dataset so I could identify the topics more accurately. After stemming and tokenizing the textual data, I calculated the best number of topics with coherence scores and then fit the dynamic topic model. To allow topics to evolve more between time slices, I also changed chain variance so it could make a difference in how the word composition changed from time slice to time slice.

### __5. Discussion__

(Please see [DTM.html](DTM.html) and [DTM.ipynb](DTM.ipynb), pyLDAvis visualizations are not kept automatically by iPython, may need to load the models and run the visualizations. And the following images serve as samples. Alternatively, the print_dtm function also prints out the same information of frequent words in different topics among years.)

---
<img src="Sector of energy.png">
&nbsp;
<img src="Sector of energy print out.png">

In the sector of energy, the best number of topics was 2. With a small chain variance (0.005), the coherence scores among three decades only held small variations, and the topic models remained the same in different time slices. After changing the chain variance to 0.5, more variations emerged. In topic 0, projects in 2000 talked more about the ‘rural’ area, and in 2010 ‘Haiti’ became the most common country in the energy projects, and when turning into 2020, ‘nature’ was one thing receiving more attention. For topic 1, in 2000 people cared more about the ‘economy’ and ‘market’, while as ‘environment’, ‘sustain’ emerged in 2010 and 2020, it might indicate that the projects had been considering the environment protection issues.

---
<img src="Sector of environment.png">
&nbsp;
<img src="Sector of environment print out.png">

In the sector of environment, the best number of topics was 3. Similarly, the topic difference among timescales was not significant when chain variance was small. After exaggerating the hyperparameter, more variations showed across the time slices. In all three topics, although there were some variations in the wording, it did not demonstrate an obvious pattern of topic changing. The only two hints were 'environment' and 'manag' ran through all three timeframes in topic 0, whereas 'climat' and 'chang' popped up in all three decades in topic 2, which might post the core guideline of the environmental projects among the three decades.

---
<img src="Sector of science and technology.png">
&nbsp;
<img src="Sector of science and technology print out.png">

In the sector of science and technology, the best number of topics went back to 2 again. And the original DTM did not show variations among time slices. After increasing the chain variance, more changes emerged in different periods. In topic 0, the frequency of ‘polici’(es), ‘innov’(ation), ‘digit’ increased in 2010 and 2020, illustrating the emphasis had moved away from that in 2000. In topic 1, the transition was slightly less obvious, but I could still see ‘knowledge’, ‘digit’, and ‘strategi’ appeared more often.

---
<img src="Sector of social investment.png">
&nbsp;
<img src="Sector of social investment print out.png">

In the sector of social investment, the best number of topics was still 2, and the coherence scores improved slightly over time and more variations emerged. From topic 0, the projects focused on ‘family’ ‘violence’, ‘gender’, and ‘poverty’ issues in 2000, turned to ‘gender’ and ‘poverty’ issues in 2010, while moved on to ‘labor’ and ‘gender’ in 2020. On the other hand, in topic 1, ‘train’(ing) might be the most important social investment in 2000, while changed into ‘health’ concern in 2010. In 2020, unsurprisingly, ‘covid’, ‘health’, ‘crisis’ were demonstrated in the terms, which clearly reflected the transition of the development projects in this sector.

---
<img src="Sector of transportation.png">
&nbsp;
<img src="Sector of transportation print out.png">

In the sector of transportation, the best number of topics was 2. With larger chain variance, ‘transport’ and ‘environment’ ran through the three decades, while ‘sustain’ and ‘mobile’ became more popular in 2010 and 2020 in topic 0, which again displayed the shift of focus in the transportation projects. As to topic 1, ‘safeti’(es) were the focal point in 2000 and 2010, whereas 2020 emphasized ‘manag’(ement) and ‘integr’(ation) in transportation.

---

In summary, the dynamic topic modeling could generally capture and reflect the transitions and patterns in development projects as described above, while it occasionally could not clearly excavate the topic changing in the dataset. Several reasons could explain the failure: first, the textual data in the same sector had high homogeneity, and those high homogeneous words tended to be with high frequency, so the model kept prioritizing these words even if I had filtered out some common words specific to this dataset. Second, the data in 2000 was less than that in 2010 or 2020, therefore, the imbalance among three textual datasets might potentially affect DTM’s ability. Also, I dropped rows with a too short description or without description and sector, which could also influence the analysis even though they only took a small portion of the dataset. Nonetheless, through this approach, DTM did provide an overview and hidden information from the project transition in different sectors.

### __Reference__

<a name="1">[1]</a>   Altaweel, M., & Hadjitofi, T. G. (2020). The sale of heritage on eBay: Market trends and cultural value. *Big Data & Society*. https://doi.org/10.1177/2053951720968865


<a name="2">[2]</a> Bonacchi, C., Altaweel, M., & Krzyzanska, M. (2018). The heritage of Brexit: Roles of the past in the construction of political identities through social media. *Journal of Social Archaeology, 18*(2), 174–192. https://doi.org/10.1177/1469605318759713

<a name="3">[3]</a> Blei, D. M., & Lafferty, J. D. (2006). Dynamic Topic Models. *Proceedings of the 23rd International Conference on Machine Learning*, 113–120. Presented at the Pittsburgh, Pennsylvania, USA. doi:10.1145/1143844.1143859

<a name="4">[4]</a> Gerrish, Sean & Blei, David. (2010). A Language-based Approach to Measuring Scholarly Impact. *ICML 2010 - Proceedings, 27th International Conference on Machine Learning*. 375-382. 

<a name="5">[5]</a> Guldi J. (2019). Parliament's Debates about Infrastructure: An Exercise in Using Dynamic Topic Models to Synthesize Historical Change. *Technology and culture, 60*(1), 1–33. https://doi.org/10.1353/tech.2019.0000

<a name="6">[6]</a> Wang, C., Blei, D. M., & Heckerman, D. (2012). Continuous Time Dynamic Topic Models. *CoRR, abs/1206.3298.* Opgehaal van http://arxiv.org/abs/1206.3298
