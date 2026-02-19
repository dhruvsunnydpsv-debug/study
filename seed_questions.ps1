# Seed CBSE Class 9 question_bank via Supabase REST API
$apikey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZWdvb2FzcnRiaHB1cnNnY3ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzOTA2NzAsImV4cCI6MjA4Njk2NjY3MH0.vV3vHZR2wqDI8WJ1zgcgJtY0J_eL21SbuE6WqciRN7s'
$base = 'https://wfegooasrtbhpursgcvh.supabase.co/rest/v1/question_bank'
$headers = @{
    'apikey' = $apikey
    'Authorization' = "Bearer $apikey"
    'Content-Type' = 'application/json'
    'Prefer' = 'return=minimal'
}

$questions = @(
    # ===== MATHS - Easy =====
    @{question_text="Find the value of (256)^(1/4)."; subject="Maths"; difficulty="Easy"; chapter="Number Systems"}
    @{question_text="Express 0.999... in the form p/q."; subject="Maths"; difficulty="Easy"; chapter="Number Systems"}
    @{question_text="Find the remainder when p(x) = x^3 + 3x^2 + 3x + 1 is divided by x + 1."; subject="Maths"; difficulty="Easy"; chapter="Polynomials"}
    @{question_text="Write the degree of the polynomial 5x^3 + 4x^2 + 7x."; subject="Maths"; difficulty="Easy"; chapter="Polynomials"}
    @{question_text="If a point lies on the x-axis, what is its y-coordinate?"; subject="Maths"; difficulty="Easy"; chapter="Coordinate Geometry"}
    @{question_text="Write the equation of x-axis."; subject="Maths"; difficulty="Easy"; chapter="Coordinate Geometry"}
    @{question_text="If one angle of a triangle is equal to the sum of the other two angles, what type of triangle is it?"; subject="Maths"; difficulty="Easy"; chapter="Lines and Angles"}
    @{question_text="In a triangle ABC, if angle A = 55 degrees and angle B = 40 degrees, find angle C."; subject="Maths"; difficulty="Easy"; chapter="Triangles"}
    @{question_text="Find the area of a triangle whose sides are 3 cm, 4 cm, and 5 cm using Heron's formula."; subject="Maths"; difficulty="Easy"; chapter="Heron's Formula"}
    @{question_text="What is the total surface area of a cube whose edge is 5 cm?"; subject="Maths"; difficulty="Easy"; chapter="Surface Areas and Volumes"}
    @{question_text="Find the mean of first 10 natural numbers."; subject="Maths"; difficulty="Easy"; chapter="Statistics"}
    @{question_text="A coin is tossed 100 times and head appears 58 times. Find the probability of getting a head."; subject="Maths"; difficulty="Easy"; chapter="Probability"}
    @{question_text="Find the value of the polynomial p(x) = 5x - 4x^2 + 3 at x = 0."; subject="Maths"; difficulty="Easy"; chapter="Polynomials"}
    @{question_text="Express the linear equation 3x + 2y = 18 in the form y = mx + c."; subject="Maths"; difficulty="Easy"; chapter="Linear Equations in Two Variables"}
    @{question_text="State Euclid's first postulate."; subject="Maths"; difficulty="Easy"; chapter="Introduction to Euclid's Geometry"}
    @{question_text="Find the circumference of a circle whose radius is 7 cm."; subject="Maths"; difficulty="Easy"; chapter="Surface Areas and Volumes"}
    @{question_text="Simplify: (3 + sqrt(3))(2 + sqrt(2))."; subject="Maths"; difficulty="Easy"; chapter="Number Systems"}
    @{question_text="Find the coordinates of the point which lies on the y-axis at a distance of 5 units above the origin."; subject="Maths"; difficulty="Easy"; chapter="Coordinate Geometry"}
    @{question_text="What is the median of 3, 7, 2, 4, 8, 1, 5?"; subject="Maths"; difficulty="Easy"; chapter="Statistics"}
    @{question_text="Name the type of quadrilateral formed by the points (3,5), (6,0), (3,-5), (0,0)."; subject="Maths"; difficulty="Easy"; chapter="Coordinate Geometry"}
    # ===== MATHS - Medium =====
    @{question_text="Factorise: 12x^2 - 7x + 1 using splitting the middle term method."; subject="Maths"; difficulty="Medium"; chapter="Polynomials"}
    @{question_text="Prove that the angles opposite to equal sides of a triangle are equal."; subject="Maths"; difficulty="Medium"; chapter="Triangles"}
    @{question_text="A triangular park has sides 120 m, 80 m and 50 m. Find its area using Heron's formula."; subject="Maths"; difficulty="Medium"; chapter="Heron's Formula"}
    @{question_text="The curved surface area of a right circular cylinder of height 14 cm is 88 cm^2. Find the diameter of the base."; subject="Maths"; difficulty="Medium"; chapter="Surface Areas and Volumes"}
    @{question_text="If two lines intersect each other, prove that vertically opposite angles are equal."; subject="Maths"; difficulty="Medium"; chapter="Lines and Angles"}
    @{question_text="Represent sqrt(9.3) on the number line."; subject="Maths"; difficulty="Medium"; chapter="Number Systems"}
    @{question_text="The taxi fare in a city is as follows: For the first kilometre, the fare is Rs 8 and for subsequent distance it is Rs 5 per km. Taking the distance covered as x km and total fare as Rs y, write a linear equation for this."; subject="Maths"; difficulty="Medium"; chapter="Linear Equations in Two Variables"}
    @{question_text="Find the volume and surface area of a sphere of radius 2.1 cm."; subject="Maths"; difficulty="Medium"; chapter="Surface Areas and Volumes"}
    @{question_text="ABCD is a parallelogram and AP and CQ are perpendiculars from vertices A and C on diagonal BD. Show that triangle APB is congruent to triangle CQD."; subject="Maths"; difficulty="Medium"; chapter="Quadrilaterals"}
    @{question_text="Construct a triangle ABC in which BC = 7 cm, angle B = 75 degrees and AB + AC = 13 cm."; subject="Maths"; difficulty="Medium"; chapter="Constructions"}
    # ===== MATHS - Hard =====
    @{question_text="Show that the line segment joining the mid-points of two sides of a triangle is parallel to the third side and is half of it."; subject="Maths"; difficulty="Hard"; chapter="Quadrilaterals"}
    @{question_text="A dome of a building is in the form of a hemisphere. From inside, it was white-washed at the cost of Rs 498.96. If the cost of white-washing is Rs 2.00 per square metre, find the inside surface area and volume of the dome."; subject="Maths"; difficulty="Hard"; chapter="Surface Areas and Volumes"}
    @{question_text="If x = 3 + 2*sqrt(2), find the value of x^2 + 1/x^2."; subject="Maths"; difficulty="Hard"; chapter="Number Systems"}
    @{question_text="In a parallelogram, show that the angle bisectors of two adjacent angles intersect at right angles."; subject="Maths"; difficulty="Hard"; chapter="Quadrilaterals"}
    @{question_text="If the polynomial az^3 + 4z^2 + 3z - 4 and z^3 - 4z + a leave the same remainder when divided by z - 3, find the value of a."; subject="Maths"; difficulty="Hard"; chapter="Polynomials"}
    @{question_text="Prove that the angle subtended by an arc at the centre is double the angle subtended by it at any point on the remaining part of the circle."; subject="Maths"; difficulty="Hard"; chapter="Circles"}
    @{question_text="A wooden bookshelf has external dimensions as follows: Height = 110 cm, Depth = 25 cm, Breadth = 85 cm. The thickness of the plank is 5 cm everywhere. The external faces are to be polished and the internal faces are to be painted. If the rate of polishing is 20 paise per cm^2 and the rate of painting is 10 paise per cm^2, find the total expenses."; subject="Maths"; difficulty="Hard"; chapter="Surface Areas and Volumes"}
    @{question_text="The following table gives the daily income of 50 workers of a factory. Find the mean daily income of the workers: Income(Rs) 100-120: 12 workers, 120-140: 14 workers, 140-160: 8 workers, 160-180: 6 workers, 180-200: 10 workers."; subject="Maths"; difficulty="Hard"; chapter="Statistics"}
    @{question_text="Three coins are tossed simultaneously 200 times with the following frequencies of different outcomes: 3 heads: 23, 2 heads: 72, 1 head: 77, No head: 28. Compute the probability of each event."; subject="Maths"; difficulty="Hard"; chapter="Probability"}
    @{question_text="Prove that equal chords of a circle subtend equal angles at the centre."; subject="Maths"; difficulty="Hard"; chapter="Circles"}
    # ===== SCIENCE - Easy =====
    @{question_text="Define the SI unit of force. Express it in terms of fundamental units."; subject="Science"; difficulty="Easy"; chapter="Force and Laws of Motion"}
    @{question_text="What is the chemical formula of baking soda?"; subject="Science"; difficulty="Easy"; chapter="Atoms and Molecules"}
    @{question_text="State Newton's first law of motion."; subject="Science"; difficulty="Easy"; chapter="Force and Laws of Motion"}
    @{question_text="What is the full form of ATP?"; subject="Science"; difficulty="Easy"; chapter="The Fundamental Unit of Life"}
    @{question_text="Name the tissue responsible for movement in our body."; subject="Science"; difficulty="Easy"; chapter="Tissues"}
    @{question_text="What is the SI unit of speed?"; subject="Science"; difficulty="Easy"; chapter="Motion"}
    @{question_text="Define an element. Give two examples."; subject="Science"; difficulty="Easy"; chapter="Is Matter Around Us Pure"}
    @{question_text="What is the function of the cell membrane?"; subject="Science"; difficulty="Easy"; chapter="The Fundamental Unit of Life"}
    @{question_text="Convert 25 degrees Celsius to Kelvin scale."; subject="Science"; difficulty="Easy"; chapter="Matter in Our Surroundings"}
    @{question_text="What is the acceleration due to gravity on the surface of the Earth?"; subject="Science"; difficulty="Easy"; chapter="Gravitation"}
    @{question_text="Define evaporation. Name the factors affecting it."; subject="Science"; difficulty="Easy"; chapter="Matter in Our Surroundings"}
    @{question_text="What are the two components of a solution?"; subject="Science"; difficulty="Easy"; chapter="Is Matter Around Us Pure"}
    @{question_text="Name the cell organelle known as the powerhouse of the cell."; subject="Science"; difficulty="Easy"; chapter="The Fundamental Unit of Life"}
    @{question_text="What is the molecular mass of water (H2O)?"; subject="Science"; difficulty="Easy"; chapter="Atoms and Molecules"}
    @{question_text="State the law of conservation of mass."; subject="Science"; difficulty="Easy"; chapter="Atoms and Molecules"}
    @{question_text="What is the unit of work?"; subject="Science"; difficulty="Easy"; chapter="Work and Energy"}
    @{question_text="Define distance and displacement. How are they different?"; subject="Science"; difficulty="Easy"; chapter="Motion"}
    @{question_text="What crops are grown in the Kharif season? Give two examples."; subject="Science"; difficulty="Easy"; chapter="Improvement in Food Resources"}
    @{question_text="Name the gas which makes up 78% of our atmosphere."; subject="Science"; difficulty="Easy"; chapter="Natural Resources"}
    @{question_text="What is the speed of sound in air at room temperature?"; subject="Science"; difficulty="Easy"; chapter="Sound"}
    # ===== SCIENCE - Medium =====
    @{question_text="Derive the equation v = u + at using the velocity-time graph."; subject="Science"; difficulty="Medium"; chapter="Motion"}
    @{question_text="A car starts from rest and acquires a velocity of 54 km/h in 2 seconds. Find (i) acceleration and (ii) distance travelled."; subject="Science"; difficulty="Medium"; chapter="Motion"}
    @{question_text="Explain the structure of an animal cell with a neat labelled diagram."; subject="Science"; difficulty="Medium"; chapter="The Fundamental Unit of Life"}
    @{question_text="How does the force of gravitation between two objects change when the distance between them is reduced to half?"; subject="Science"; difficulty="Medium"; chapter="Gravitation"}
    @{question_text="Calculate the number of moles in 52 g of He (atomic mass of He = 4u)."; subject="Science"; difficulty="Medium"; chapter="Atoms and Molecules"}
    @{question_text="Differentiate between compound and mixture. Give three differences."; subject="Science"; difficulty="Medium"; chapter="Is Matter Around Us Pure"}
    @{question_text="What is the difference between striated, unstriated, and cardiac muscle fibres?"; subject="Science"; difficulty="Medium"; chapter="Tissues"}
    @{question_text="Explain how sound is produced and how it is transmitted through a medium."; subject="Science"; difficulty="Medium"; chapter="Sound"}
    @{question_text="A body of mass 25 kg has a momentum of 125 kg m/s. Calculate the velocity of the body."; subject="Science"; difficulty="Medium"; chapter="Force and Laws of Motion"}
    @{question_text="What is an echo? What are the conditions necessary for an echo to be heard?"; subject="Science"; difficulty="Medium"; chapter="Sound"}
    # ===== SCIENCE - Hard =====
    @{question_text="State and explain Newton's third law of motion. Give an example of a case where the action and reaction forces act on different bodies."; subject="Science"; difficulty="Hard"; chapter="Force and Laws of Motion"}
    @{question_text="The brakes applied to a car produce a deceleration of 6 m/s^2 in the opposite direction to the motion. If the car takes 2 seconds to stop after the application of brakes, calculate the distance it travels during this time."; subject="Science"; difficulty="Hard"; chapter="Motion"}
    @{question_text="In a reaction, 5.3 g of sodium carbonate reacted with 6 g of ethanoic acid. The products were 2.2 g of carbon dioxide, 0.9 g of water and 8.2 g of sodium ethanoate. Show that these observations are in agreement with the law of conservation of mass."; subject="Science"; difficulty="Hard"; chapter="Atoms and Molecules"}
    @{question_text="Two objects of masses 100 g and 200 g are moving along the same line and direction with velocities of 2 m/s and 1 m/s respectively. They collide and after collision, the first object moves at a velocity of 1.67 m/s. Determine the velocity of the second object."; subject="Science"; difficulty="Hard"; chapter="Force and Laws of Motion"}
    @{question_text="Describe the nitrogen cycle in nature. Draw a diagram to support your answer."; subject="Science"; difficulty="Hard"; chapter="Natural Resources"}
    @{question_text="A stone is thrown vertically upward with an initial velocity of 40 m/s. Taking g = 10 m/s^2, find (i) the maximum height reached, (ii) the total time of journey, and (iii) the velocity of the stone on reaching the ground."; subject="Science"; difficulty="Hard"; chapter="Gravitation"}
    @{question_text="Explain the process of dialysis and its significance in understanding osmosis."; subject="Science"; difficulty="Hard"; chapter="The Fundamental Unit of Life"}
    @{question_text="Explain why the ceiling fan continues to rotate for some time even after it has been switched off."; subject="Science"; difficulty="Hard"; chapter="Force and Laws of Motion"}
    @{question_text="The kinetic energy of an object of mass m moving with a velocity of 5 m/s is 25 J. What will be its kinetic energy when its velocity is doubled? What will be its kinetic energy when its velocity is increased three times?"; subject="Science"; difficulty="Hard"; chapter="Work and Energy"}
    @{question_text="Explain Archimedes' principle and state two applications of it."; subject="Science"; difficulty="Hard"; chapter="Gravitation"}
    # ===== SOCIAL SCIENCE - Easy =====
    @{question_text="What is democracy? Define it in your own words."; subject="Social Science"; difficulty="Easy"; chapter="What is Democracy"}
    @{question_text="Name the three major religions that originated in India."; subject="Social Science"; difficulty="Easy"; chapter="India: Size and Location"}
    @{question_text="What is the Tropic of Cancer? State its latitude."; subject="Social Science"; difficulty="Easy"; chapter="India: Size and Location"}
    @{question_text="When did the French Revolution begin?"; subject="Social Science"; difficulty="Easy"; chapter="The French Revolution"}
    @{question_text="What is poverty line? How is it defined?"; subject="Social Science"; difficulty="Easy"; chapter="Poverty as a Challenge"}
    @{question_text="Name the highest peak of the Himalayas."; subject="Social Science"; difficulty="Easy"; chapter="Physical Features of India"}
    @{question_text="What is the literacy rate of India according to the 2011 Census?"; subject="Social Science"; difficulty="Easy"; chapter="Population"}
    @{question_text="Define the term 'apartheid'."; subject="Social Science"; difficulty="Easy"; chapter="Democracy in the Contemporary World"}
    @{question_text="What are the three parallel ranges of the Himalayas?"; subject="Social Science"; difficulty="Easy"; chapter="Physical Features of India"}
    @{question_text="What is the meaning of 'Ancien Regime'?"; subject="Social Science"; difficulty="Easy"; chapter="The French Revolution"}
    @{question_text="Name two seasonal rivers of India."; subject="Social Science"; difficulty="Easy"; chapter="Drainage"}
    @{question_text="What is Green Revolution?"; subject="Social Science"; difficulty="Easy"; chapter="Food Security in India"}
    @{question_text="Who was the first President of independent India?"; subject="Social Science"; difficulty="Easy"; chapter="Constitutional Design"}
    @{question_text="What is the tenure of the members of Rajya Sabha?"; subject="Social Science"; difficulty="Easy"; chapter="Working of Institutions"}
    @{question_text="Define 'human capital'."; subject="Social Science"; difficulty="Easy"; chapter="People as Resource"}
    @{question_text="What is a Tsunami?"; subject="Social Science"; difficulty="Easy"; chapter="Physical Features of India"}
    @{question_text="Name the river known as the 'Sorrow of Bengal'."; subject="Social Science"; difficulty="Easy"; chapter="Drainage"}
    @{question_text="Which season in India is known as the retreating monsoon season?"; subject="Social Science"; difficulty="Easy"; chapter="Climate"}
    @{question_text="What is the election commission of India?"; subject="Social Science"; difficulty="Easy"; chapter="Electoral Politics"}
    @{question_text="What are the main food crops of India?"; subject="Social Science"; difficulty="Easy"; chapter="Food Security in India"}
    # ===== SOCIAL SCIENCE - Medium =====
    @{question_text="Describe the role of women during the French Revolution."; subject="Social Science"; difficulty="Medium"; chapter="The French Revolution"}
    @{question_text="Explain the formation of the Himalayan mountain ranges."; subject="Social Science"; difficulty="Medium"; chapter="Physical Features of India"}
    @{question_text="What are the main features of the Indian Constitution?"; subject="Social Science"; difficulty="Medium"; chapter="Constitutional Design"}
    @{question_text="Describe the monsoon mechanism in India."; subject="Social Science"; difficulty="Medium"; chapter="Climate"}
    @{question_text="Explain the causes and effects of poverty in India."; subject="Social Science"; difficulty="Medium"; chapter="Poverty as a Challenge"}
    @{question_text="What is the difference between Lok Sabha and Rajya Sabha? Give five differences."; subject="Social Science"; difficulty="Medium"; chapter="Working of Institutions"}
    @{question_text="Describe the major peninsular rivers of India and their characteristics."; subject="Social Science"; difficulty="Medium"; chapter="Drainage"}
    @{question_text="Explain the events leading to the storming of the Bastille on 14 July 1789."; subject="Social Science"; difficulty="Medium"; chapter="The French Revolution"}
    @{question_text="What are the advantages and disadvantages of democracy?"; subject="Social Science"; difficulty="Medium"; chapter="What is Democracy"}
    @{question_text="Explain the concept of sustainable development with examples."; subject="Social Science"; difficulty="Medium"; chapter="People as Resource"}
    # ===== SOCIAL SCIENCE - Hard =====
    @{question_text="Critically examine the reign of terror during the French Revolution. What was its impact on the revolution?"; subject="Social Science"; difficulty="Hard"; chapter="The French Revolution"}
    @{question_text="Discuss the challenges to democracy in India with reference to poverty, illiteracy, and social inequality."; subject="Social Science"; difficulty="Hard"; chapter="What is Democracy"}
    @{question_text="Explain the drainage pattern of India. How are the Himalayan rivers different from the Peninsular rivers? Compare in detail with examples."; subject="Social Science"; difficulty="Hard"; chapter="Drainage"}
    @{question_text="What role did Nelson Mandela play in establishing democracy in South Africa? What lessons can India learn from his struggle?"; subject="Social Science"; difficulty="Hard"; chapter="Democracy in the Contemporary World"}
    @{question_text="Describe how the Indian monsoon operates. What are the factors that influence the onset and withdrawal of monsoons in India?"; subject="Social Science"; difficulty="Hard"; chapter="Climate"}
    # ===== ENGLISH - Easy =====
    @{question_text="What is a synonym? Give synonyms of: beautiful, happy, big."; subject="English"; difficulty="Easy"; chapter="Grammar"}
    @{question_text="Change the following sentence to passive voice: 'She writes a letter every day.'"; subject="English"; difficulty="Easy"; chapter="Grammar"}
    @{question_text="Fill in the blank with the correct article: ___ Taj Mahal is in Agra."; subject="English"; difficulty="Easy"; chapter="Grammar"}
    @{question_text="What is the moral of the story 'The Lost Child'?"; subject="English"; difficulty="Easy"; chapter="The Lost Child"}
    @{question_text="What did the child want to eat at the fair in the story 'The Lost Child'?"; subject="English"; difficulty="Easy"; chapter="The Lost Child"}
    @{question_text="Who wrote the poem 'The Road Not Taken'?"; subject="English"; difficulty="Easy"; chapter="The Road Not Taken"}
    @{question_text="What does the poet mean by 'two roads diverged in a yellow wood'?"; subject="English"; difficulty="Easy"; chapter="The Road Not Taken"}
    @{question_text="Define a compound sentence. Give an example."; subject="English"; difficulty="Easy"; chapter="Grammar"}
    @{question_text="What is the meaning of the word 'tranquil'?"; subject="English"; difficulty="Easy"; chapter="Grammar"}
    @{question_text="Identify the subject and predicate: 'The quick brown fox jumps over the lazy dog.'"; subject="English"; difficulty="Easy"; chapter="Grammar"}
    @{question_text="Who is the author of 'The Fun They Had'?"; subject="English"; difficulty="Easy"; chapter="The Fun They Had"}
    @{question_text="What kind of school does Margie have in 'The Fun They Had'?"; subject="English"; difficulty="Easy"; chapter="The Fun They Had"}
    @{question_text="Change to indirect speech: He said, 'I am going to school.'"; subject="English"; difficulty="Easy"; chapter="Grammar"}
    @{question_text="What is an adjective? Give three examples."; subject="English"; difficulty="Easy"; chapter="Grammar"}
    @{question_text="Use the word 'although' in a sentence."; subject="English"; difficulty="Easy"; chapter="Grammar"}
    @{question_text="What did the swallow do for the Happy Prince?"; subject="English"; difficulty="Easy"; chapter="The Happy Prince"}
    @{question_text="Who was Bismillah Khan? What instrument did he play?"; subject="English"; difficulty="Easy"; chapter="The Sound of Music"}
    @{question_text="What does Tommy find in the story 'The Fun They Had'?"; subject="English"; difficulty="Easy"; chapter="The Fun They Had"}
    @{question_text="Correct the sentence: 'She don't know nothing about it.'"; subject="English"; difficulty="Easy"; chapter="Grammar"}
    @{question_text="What is the difference between 'their', 'there', and 'they're'?"; subject="English"; difficulty="Easy"; chapter="Grammar"}
    # ===== ENGLISH - Medium =====
    @{question_text="Write a paragraph (100-150 words) on 'The Importance of Reading'."; subject="English"; difficulty="Medium"; chapter="Writing"}
    @{question_text="Write a letter to the editor of a newspaper about the increasing pollution in your city."; subject="English"; difficulty="Medium"; chapter="Writing"}
    @{question_text="Explain the central theme of the poem 'The Road Not Taken' by Robert Frost."; subject="English"; difficulty="Medium"; chapter="The Road Not Taken"}
    @{question_text="What role does the Happy Prince's sapphire eyes play in the story? What do they symbolize?"; subject="English"; difficulty="Medium"; chapter="The Happy Prince"}
    @{question_text="How did Evelyn Glennie's hearing impairment not come in the way of her musical career? Discuss."; subject="English"; difficulty="Medium"; chapter="The Sound of Music"}
    @{question_text="Transform the following sentences into complex sentences: (a) He is too weak to walk. (b) Work hard or you will fail."; subject="English"; difficulty="Medium"; chapter="Grammar"}
    @{question_text="Write a diary entry expressing your feelings after winning a sports competition."; subject="English"; difficulty="Medium"; chapter="Writing"}
    @{question_text="What is the irony in the title 'The Fun They Had'?"; subject="English"; difficulty="Medium"; chapter="The Fun They Had"}
    @{question_text="Describe the physical suffering of the child as he walks through the fair in 'The Lost Child'."; subject="English"; difficulty="Medium"; chapter="The Lost Child"}
    @{question_text="Convert the following to reported speech: 'Will you help me with my homework?' she asked."; subject="English"; difficulty="Medium"; chapter="Grammar"}
    # ===== ENGLISH - Hard =====
    @{question_text="'The Road Not Taken' is not simply a poem about choosing a path in the woods. It is a metaphor for making life choices. Discuss in 200 words."; subject="English"; difficulty="Hard"; chapter="The Road Not Taken"}
    @{question_text="Write a story in 200-250 words beginning with: 'It was a dark and stormy night when the doorbell rang...'"; subject="English"; difficulty="Hard"; chapter="Writing"}
    @{question_text="What is the message of the story 'The Happy Prince'? How does Oscar Wilde use the characters to explore themes of sacrifice and compassion?"; subject="English"; difficulty="Hard"; chapter="The Happy Prince"}
    @{question_text="Write an article for your school magazine on the topic 'Technology: A Boon or a Bane' in 200-250 words."; subject="English"; difficulty="Hard"; chapter="Writing"}
    @{question_text="Compare and contrast the educational system described in 'The Fun They Had' with the current education system. Which one would you prefer and why?"; subject="English"; difficulty="Hard"; chapter="The Fun They Had"}
    # ===== HINDI - Easy =====
    @{question_text="'दो बैलों की कथा' पाठ में हीरा और मोती के चरित्र की एक विशेषता बताइए।"; subject="Hindi"; difficulty="Easy"; chapter="Do Bailon Ki Katha"}
    @{question_text="'ल्हासा की ओर' पाठ के लेखक का नाम बताइए।"; subject="Hindi"; difficulty="Easy"; chapter="Lhasa Ki Or"}
    @{question_text="संधि किसे कहते हैं? उदाहरण सहित बताइए।"; subject="Hindi"; difficulty="Easy"; chapter="Hindi Vyakaran"}
    @{question_text="विलोम शब्द लिखिए: (क) सुख (ख) दिन (ग) जीवन"; subject="Hindi"; difficulty="Easy"; chapter="Hindi Vyakaran"}
    @{question_text="'साँवले सपनों की याद' पाठ में लेखक ने किसकी याद की बात कही है?"; subject="Hindi"; difficulty="Easy"; chapter="Sanwale Sapnon Ki Yaad"}
    @{question_text="'नाना साहब की पुत्री देवी मैना को भस्म कर दिया गया' पाठ में मैना कौन थी?"; subject="Hindi"; difficulty="Easy"; chapter="Nana Sahab Ki Putri"}
    @{question_text="पर्यायवाची शब्द लिखिए: (क) पानी (ख) फूल (ग) आकाश"; subject="Hindi"; difficulty="Easy"; chapter="Hindi Vyakaran"}
    @{question_text="सर्वनाम किसे कहते हैं? उदाहरण दीजिए।"; subject="Hindi"; difficulty="Easy"; chapter="Hindi Vyakaran"}
    @{question_text="'कबीर दास' के दोहे का अर्थ लिखिए: 'पोथी पढ़ पढ़ जग मुआ, पंडित भया न कोई'"; subject="Hindi"; difficulty="Easy"; chapter="Kabir"}
    @{question_text="मुहावरे का अर्थ लिखिए: 'आँखों में धूल झोंकना'"; subject="Hindi"; difficulty="Easy"; chapter="Hindi Vyakaran"}
    @{question_text="रस किसे कहते हैं? कितने प्रकार के होते हैं?"; subject="Hindi"; difficulty="Easy"; chapter="Hindi Vyakaran"}
    @{question_text="'उपसर्ग' किसे कहते हैं? दो उदाहरण दीजिए।"; subject="Hindi"; difficulty="Easy"; chapter="Hindi Vyakaran"}
    @{question_text="निम्नलिखित शब्दों में से तत्सम और तद्भव शब्द चुनिए: दूध, क्षीर, अग्नि, आग"; subject="Hindi"; difficulty="Easy"; chapter="Hindi Vyakaran"}
    @{question_text="'क्या निराश हुआ जाए' पाठ का मुख्य संदेश क्या है?"; subject="Hindi"; difficulty="Easy"; chapter="Kya Nirash Hua Jaye"}
    @{question_text="वाक्य शुद्ध करो: 'मुझे किताब को पढ़ना है'"; subject="Hindi"; difficulty="Easy"; chapter="Hindi Vyakaran"}
    @{question_text="'समास' किसे कहते हैं? एक उदाहरण दीजिए।"; subject="Hindi"; difficulty="Easy"; chapter="Hindi Vyakaran"}
    @{question_text="'अलंकार' किसे कहते हैं? 'उपमा अलंकार' का उदाहरण दीजिए।"; subject="Hindi"; difficulty="Easy"; chapter="Hindi Vyakaran"}
    @{question_text="निबंध के लिए प्रस्तावना कैसे लिखें?"; subject="Hindi"; difficulty="Easy"; chapter="Hindi Vyakaran"}
    @{question_text="'ग्राम श्री' कविता का केंद्रीय भाव क्या है?"; subject="Hindi"; difficulty="Easy"; chapter="Gram Shree"}
    @{question_text="संज्ञा के कितने भेद हैं? नाम लिखिए।"; subject="Hindi"; difficulty="Easy"; chapter="Hindi Vyakaran"}
    # ===== HINDI - Medium =====
    @{question_text="'दो बैलों की कथा' में प्रेमचंद ने किस प्रकार पशुओं के माध्यम से मानवीय मूल्यों को प्रस्तुत किया है? वर्णन कीजिए।"; subject="Hindi"; difficulty="Medium"; chapter="Do Bailon Ki Katha"}
    @{question_text="'ल्हासा की ओर' पाठ में लेखक ने तिब्बत की यात्रा का वर्णन कैसे किया है? मुख्य बिंदु लिखिए।"; subject="Hindi"; difficulty="Medium"; chapter="Lhasa Ki Or"}
    @{question_text="अपने विद्यालय के प्रधानाचार्य को पुस्तकालय में नई पुस्तकें मंगवाने के लिए आवेदन पत्र लिखिए।"; subject="Hindi"; difficulty="Medium"; chapter="Patra Lekhan"}
    @{question_text="'महादेवी वर्मा' द्वारा रचित 'मेरे बचपन के दिन' पाठ का सारांश अपने शब्दों में लिखिए।"; subject="Hindi"; difficulty="Medium"; chapter="Mere Bachpan Ke Din"}
    @{question_text="'वाच्य' किसे कहते हैं? कर्तृवाच्य और कर्मवाच्य में अंतर बताइए, उदाहरण सहित।"; subject="Hindi"; difficulty="Medium"; chapter="Hindi Vyakaran"}
    # ===== HINDI - Hard =====
    @{question_text="'प्रेमचंद की कहानियों में सामाजिक चेतना' विषय पर 250 शब्दों में निबंध लिखिए।"; subject="Hindi"; difficulty="Hard"; chapter="Nibandh"}
    @{question_text="'दो बैलों की कथा' और 'ईदगाह' कहानियों की तुलना करते हुए प्रेमचंद की कथा-शिल्प पर प्रकाश डालिए।"; subject="Hindi"; difficulty="Hard"; chapter="Do Bailon Ki Katha"}
    @{question_text="'कबीर दास और रहीम' के दोहों की तुलना करते हुए बताइए कि दोनों कवियों के काव्य में क्या समानताएँ और विभिन्नताएँ हैं।"; subject="Hindi"; difficulty="Hard"; chapter="Kabir"}
    # ===== COMPUTER SCIENCE - Easy =====
    @{question_text="What is an operating system? Name any two popular operating systems."; subject="Computer Science"; difficulty="Easy"; chapter="Computer Systems"}
    @{question_text="What is the full form of CPU? What are its components?"; subject="Computer Science"; difficulty="Easy"; chapter="Computer Systems"}
    @{question_text="Define the term 'algorithm'. Give a simple example."; subject="Computer Science"; difficulty="Easy"; chapter="Algorithms and Flowcharts"}
    @{question_text="What is the difference between hardware and software?"; subject="Computer Science"; difficulty="Easy"; chapter="Computer Systems"}
    @{question_text="Convert the decimal number 25 to binary."; subject="Computer Science"; difficulty="Easy"; chapter="Number Systems"}
    @{question_text="What is a flowchart? What are the basic symbols used in a flowchart?"; subject="Computer Science"; difficulty="Easy"; chapter="Algorithms and Flowcharts"}
    @{question_text="Name three input devices and three output devices."; subject="Computer Science"; difficulty="Easy"; chapter="Computer Systems"}
    @{question_text="What is the difference between RAM and ROM?"; subject="Computer Science"; difficulty="Easy"; chapter="Computer Systems"}
    @{question_text="What is the Internet? Name two popular web browsers."; subject="Computer Science"; difficulty="Easy"; chapter="Internet and Web"}
    @{question_text="Define the term 'variable' in programming. Give an example."; subject="Computer Science"; difficulty="Easy"; chapter="Introduction to Python"}
    @{question_text="What is HTML? What does it stand for?"; subject="Computer Science"; difficulty="Easy"; chapter="Internet and Web"}
    @{question_text="Name three types of cyber threats."; subject="Computer Science"; difficulty="Easy"; chapter="Cyber Safety"}
    @{question_text="What is the purpose of an antivirus software?"; subject="Computer Science"; difficulty="Easy"; chapter="Cyber Safety"}
    @{question_text="List three advantages of using a computer."; subject="Computer Science"; difficulty="Easy"; chapter="Computer Systems"}
    @{question_text="What is a byte? How many bits make a byte?"; subject="Computer Science"; difficulty="Easy"; chapter="Number Systems"}
    @{question_text="What is the output of the following Python code: print(3 + 4 * 2)?"; subject="Computer Science"; difficulty="Easy"; chapter="Introduction to Python"}
    @{question_text="What is a compiler? How is it different from an interpreter?"; subject="Computer Science"; difficulty="Easy"; chapter="Computer Systems"}
    @{question_text="Define 'phishing' in terms of cyber security."; subject="Computer Science"; difficulty="Easy"; chapter="Cyber Safety"}
    @{question_text="What is the function of a printer?"; subject="Computer Science"; difficulty="Easy"; chapter="Computer Systems"}
    @{question_text="What is Python? Name two features of Python programming language."; subject="Computer Science"; difficulty="Easy"; chapter="Introduction to Python"}
    # ===== COMPUTER SCIENCE - Medium =====
    @{question_text="Write a Python program to find the largest of three numbers entered by the user."; subject="Computer Science"; difficulty="Medium"; chapter="Introduction to Python"}
    @{question_text="Explain the difference between LAN, MAN, and WAN with examples."; subject="Computer Science"; difficulty="Medium"; chapter="Internet and Web"}
    @{question_text="Convert the binary number 11011 to decimal. Show the steps."; subject="Computer Science"; difficulty="Medium"; chapter="Number Systems"}
    @{question_text="Draw a flowchart to calculate the area of a rectangle."; subject="Computer Science"; difficulty="Medium"; chapter="Algorithms and Flowcharts"}
    @{question_text="Write an algorithm to check whether a given number is even or odd."; subject="Computer Science"; difficulty="Medium"; chapter="Algorithms and Flowcharts"}
    @{question_text="What are the different data types in Python? Explain with examples."; subject="Computer Science"; difficulty="Medium"; chapter="Introduction to Python"}
    @{question_text="Write a Python program to print the Fibonacci series up to n terms."; subject="Computer Science"; difficulty="Medium"; chapter="Introduction to Python"}
    @{question_text="Explain the concept of digital footprint. How can you protect your digital footprint?"; subject="Computer Science"; difficulty="Medium"; chapter="Cyber Safety"}
    @{question_text="What is the difference between a virus, a worm, and a trojan horse?"; subject="Computer Science"; difficulty="Medium"; chapter="Cyber Safety"}
    @{question_text="Write a Python program that takes marks of 5 subjects as input and calculates the percentage."; subject="Computer Science"; difficulty="Medium"; chapter="Introduction to Python"}
    # ===== COMPUTER SCIENCE - Hard =====
    @{question_text="Write a Python program to check whether a number is a palindrome or not. Also draw the flowchart."; subject="Computer Science"; difficulty="Hard"; chapter="Introduction to Python"}
    @{question_text="Explain the OSI model of networking. Describe each layer and its function."; subject="Computer Science"; difficulty="Hard"; chapter="Internet and Web"}
    @{question_text="Compare and contrast cloud computing and edge computing. What are the advantages and disadvantages of each?"; subject="Computer Science"; difficulty="Hard"; chapter="Internet and Web"}
    @{question_text="Write a Python program that uses a loop to print all prime numbers between 1 and 100."; subject="Computer Science"; difficulty="Hard"; chapter="Introduction to Python"}
    @{question_text="What are the ethical issues in computing? Discuss software piracy, plagiarism, and data privacy in detail."; subject="Computer Science"; difficulty="Hard"; chapter="Cyber Safety"}
)

Write-Host "🚀 Seeding $($questions.Count) questions into question_bank..."

$success = 0
$failed = 0

foreach ($q in $questions) {
    $body = $q | ConvertTo-Json -Compress
    try {
        Invoke-RestMethod -Uri $base -Headers $headers -Method Post -Body $body | Out-Null
        $success++
    } catch {
        $failed++
        if ($failed -le 3) {
            $err = $_.Exception.Response
            try { $sr = [System.IO.StreamReader]::new($err.GetResponseStream()); Write-Host "  Error: $($sr.ReadToEnd())" } catch { Write-Host "  Error: $_" }
        }
    }
}

Write-Host "✅ Done! Inserted: $success, Failed: $failed"
