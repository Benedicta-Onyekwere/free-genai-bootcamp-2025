## Perplexity Powered Assistant Guide

### Which Model
Perplexity Pro uses their own model by default, but specific models can be chosen in user settings. The model i used is the free version Perplexity AI.

https://www.perplexity.ai/hub/technical-faq/what-model-does-perplexity-use-and-what-is-the-perplexity-model

https://www.perplexity.ai/hub/technical-faq/what-advanced-ai-models-does-perplexity-pro-unlock

We also explored Deepseek R-1 and OpenAI's o3-mini in the spanish sentence constructor video.

### Prompting Guides

https://www.perplexity.ai/hub/faq/prompting-tips-and-examples-on-perplexity

It appears that Perplexity does not have any special prompting requirements (XML, markdown) to best understand context like other models.

## Perplexity Prompt Observation
The model performed as expected, it was brief and straight to the point. it gave a sentence in english and asked me to translate it to spanish.

It also gave the vocubulary table for the sentence it wanted me to translate to spanish, sentence structure and only two clues and considerations as instructed.


### Answer  

Here is your sentence to translate into Spanish:
"The professor is explaining the complex theory to the students."

| Spanish  | English   |
|----------|----------|
| profesor | professor |
| explicar | to explain |
| teoría   | theory    |
| estudiante | student  |

#### **Sentence Structure**
[Subject] [Verb] [Object] [Preposition] [Object].

#### **Clues and Considerations**
- Consider the verb tense that fits the context of the sentence.
- Think about how to express "to the students" in Spanish, considering prepositions and word order.

I got the translation of the above from chagpt which is **"El profesor está explicando la teoría compleja a los estudiantes"**, below is the result it gave me:




### Answer  
Your translation, *"El profesor está explicando la teoría compleja a los estudiantes,"* is mostly correct. However, the original sentence is *"The professor is explaining the complex theory to the students."* In Spanish, the definite article *"the"* is translated as *"la"* for feminine nouns like *"teoría,"* but the word order and adjective placement are slightly different. The correct translation should be *"El profesor está explicando la teoría compleja a los estudiantes,"* which you provided.  

However, if you want to emphasize that it is a specific theory, you might consider using *"la teoría compleja"* as you did. The sentence is grammatically correct and conveys the intended meaning.  

It then asked me to translate another sentence as instructed in the prompt when i get the correct spanish translation.
 

## Deepseek R-1 Prompt Observation

Using the same prompt instructions for this model, the model was quite interesting and facinating and very different from all the other models because it thinks out loud, in the sense that it keeps writing how its reasoning before giving its final answer this is shown below:

### Thinking...

Okay, the user is a Spanish teacher helping a student at C1 level. The task is to get the student to transcribe an English sentence into Spanish without giving the answer directly. The student needs to work through clues. Let me start by understanding the process.

First, I need to provide a vocabulary table with relevant words in their dictionary forms. The table should have Spanish and English columns, no more than 1-3 rows. Then, give a possible sentence structure using placeholders like [Subject], [Verb], etc., without conjugations. Clues should be minimal, maybe just a couple of points.

The example given earlier for the sentence *"The raven is in the garden, and it is looking at the flowers."* used a structure with two clauses connected by *"and"*. So for each new sentence, I need to break down structure similarly.

Wait, the user mentioned *"once the student has successfully translated the sentence, prompt them with a new sentence."* So after they get it right, move on to another one. But for now, the first sentence hasn't been provided yet. Let me check the user's instructions again.

The initial instruction says: *"You will provide the student a sentence that aligns with the prompted language level."* So the assistant's first step is to present a sentence in English for the student to translate into Spanish. The assistant then provides a vocabulary table, structure, and clues. When the student attempts, the assistant interprets their attempt and gives feedback, then moves on once correct.

---

The user's example starts with the assistant giving a sentence, then the student works through it. Let me think of a C1-level sentence. Since C1 is advanced, maybe a complex structure with subjunctive or conditional? For example:  
*"If I had known, I would have arrived earlier."*

But let's start with the example given in the instructions:  
*"I saw the raven because it was loud."*  

The structure given is:  
**[Subject] [Verb] [Object] [Subordinating Conjunction] [Subject] [Verb] [Adjective].**  

So for a C1 sentence, perhaps a conditional or a compound sentence with a subordinate clause.

Another example:  
*"Although she was tired, she continued working on the project."*  
Structure:  
**[Subordinating Conjunction] [Subject] [Verb] [Adjective], [Subject] [Verb] [Preposition] [Object].**  

Wait, but the user said to consider beginner structures in the sentence structure part. Wait, no: the example given includes structures like *"This morning, I saw the raven."* which is a time phrase followed by a simple sentence. But for C1, maybe more complex structures. Hmm, but the teaching instruction says *"remember to consider beginner level sentence structures"* in the sentence structure part. That seems conflicting.  

---

Wait, perhaps the sentence structure part is supposed to be the breakdown of the target sentence into components, regardless of the student's level, but using placeholders. So the structure would abstract away the complexity, allowing the student to apply the correct grammar.

For example, a sentence like:  
*"Had I known about the meeting, I wouldn't have missed it."*  
Structure:  
**[Past Perfect Clause], [Subject] [Conditional Verb] [Verb] [Object].**  

But maybe that's too detailed. Alternatively, using more general terms:  

For a C1 sentence, let's go with a third conditional:  
*"If I had more time, I would travel the world."*  

#### Vocabulary Table:
| Spanish | English  |
|---------|---------|
| tiempo  | time    |
| viajar  | to travel |
| mundo   | world   |

#### Sentence Structure:
**[If] [Subject] [Verb] [Adjective] [Noun], [Subject] [Conditional Verb] [Verb] [Object].**  

#### Clues and Considerations:
- The conditional *"would"* requires the conditional tense in Spanish.  
- The *"if"* clause uses the imperfect subjunctive.  

---

But wait, the structure part shouldn't mention tenses, right? The instruction says *"do not provide tenses or conjugations in the sentence structure"*. So the structure would be more like:  

**[If Clause], [Main Clause].**  

Breaking it into parts:

Structure:  
**[If] [Subject] [Verb] [Adjective] [Noun], [Subject] [Verb] [Verb] [Object].**  

However, the main clause uses a conditional verb, so perhaps that should be indicated.  

---

The student attempts to translate. Suppose they write:  
*"Si yo tenía más tiempo, yo viajaría el mundo."*  

The assistant would interpret this as:  
*"If I had (imperfect indicative) more time, I would travel the world."*  

Then, point out that the verb in the *"if"* clause should be in the imperfect subjunctive, not the indicative. The correct form is **"tuviera"**. Also, *"viajar el mundo"* should be *"viajar por el mundo"* or *"recorrer el mundo"*, but the preposition might be tricky. However, the main issue is the verb tense.

The assistant would say:  
*"Your attempt uses 'tenía' in the 'if' clause, which is the imperfect indicative. However, hypothetical 'if' clauses in Spanish require the imperfect subjunctive. Also, consider the preposition after 'viajar' when referring to traveling around the world."*

The student might then correct to:  
**"Si tuviera más tiempo, viajaría por el mundo."**  

The assistant confirms and provides a new sentence.  

---

### Next Sentence Example:
*"She told me that she would have finished the report by Friday."*  

But let's stick to the initial example and process. The key is to follow the structure and clues without giving away the answer. The assistant must encourage the student to think through the grammar and vocabulary, using the provided tools.

Another example sentence for after the first one:  
*"Had I arrived earlier, I wouldn't have missed the meeting."*  

But again, ensuring the vocabulary and structure are appropriate.

---

### Summary:
The assistant's role is to guide the student through each step, providing only the necessary scaffolding for them to construct the Spanish sentence correctly, using their existing knowledge and the provided clues.

---

#### Vocabulary Table:
| Spanish | English  |
|---------|---------|
| tiempo  | time    |
| viajar  | to travel |
| mundo   | world   |

#### Sentence Structure:
**[If] [Subject] [Verb] [Adjective] [Noun], [Subject] [Conditional Verb] [Verb] [Object].**  

#### Clues and Considerations:
- The verb in the *"if"* clause requires a specific tense for hypothetical situations.  
- The main clause’s auxiliary verb is in the conditional form.


## OpenAI's o3-mini Prompt Observation
This model worked same as perplexity, giving brief and straight to the point answer. this is shown below:

Here is your challenge sentence in English:

*“The diligent student carefully analyzed the complex text.”*

### Vocabulary Table
| Spanish    | English  |
|------------|---------|
| estudiante | student |
| analizar   | to analyze |
| complejo   | complex |

### Sentence Structure
[Determiner] [Subject] [Adjective] [Adverb] [Verb] [Determiner] [Adjective] [Object]

### Clues and Considerations
- Consider where adjectives typically appear relative to the noun they modify.
- Recall that adverbs usually come before the verb in Spanish.

Now, please try transcribing the sentence into Spanish.
