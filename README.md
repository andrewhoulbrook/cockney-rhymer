# Cockney Rhymer

A script to generate Cockney rhyming slang-style phrase constructions (just for fun).

## Rhyming Slang

Rhyming slang, Cockney rhyming slang most famously, is a humorous slang construction in the English language. Cockney rhyming slang is believed to originate from London's East End in the mid-nineteenth century. Whether rhyming slang emerged by linguistic accident, was a game that became popular or a deliberate cyptolect remains open to speculation. 

<p align="center">
  <img src="/doc/diamond_geezer.jpg"/>
</p>

Rhyming slang continues to evolve with the more modern **Mockney**. You can read more about the history Cockney rhyming slang [here](https://www.cockneyrhymingslang.co.uk/blog/what-is-cockney-rhyming-slang/).

### Rhyme Structure

Rhyming slang is constructed using a pair of associated words (collocations) and where the second word rhymes with the word that you intend to use. However, it's typically the first word rather than the second (rhyming) word which is then used as a substitute for the intended word, with the second (rhyming) word omitted. This traditional construction of rhyming slang is used in this script.

E.g. "butcher's hook" where "hook" rhymes with "look" which can used to construct the rhyming phrase "Have a butcher's at this." There's also the classic "apples and pears" where "pears" rhymes with "stairs" used as "I'm going up the apples."

While typically the rhyming word is omitted, it's not always the case. E.g. "boat race" where "race" rhymes with "face" is more commonly used as "did you see his boat race?" rather than "did you see his boat?" The use of "Giraffe" for "Laugh" is another irregular example. 

<p align="center">
  <img src="/doc/sign.jpg"/>
</p>

Rhyming slang can be characterized as either phonetic or phono-semantic in form. This script is built around phonetic forms of rhyming slang only. Authentic Cockney rhyming slang doesn't only consist of rhyme associations; many of the Cockney expressions also have rich semantic links [read more here](https://www.theguardian.com/education/2014/jun/09/guide-to-cockney-rhyming-slang).

### How cockneyRhymer.py Works

This script uses NLTK to tokenize and then tag each word within the user's input text. Tagged nouns are selected and then reduced to base form (via lemmatization). This may be worth experimenting with, as it's the lemma that will be used to find rhyme words. Sometimes this will not be optimal. The idea was that in reduced form, finding rhyming matches would be easier.  

This script doesn't implement any rhyming algorithm itself (no trivial task), rather it uses the mastery of the [DataMuse API Service's](https://www.datamuse.com/api/) rhyming algorithms. Each noun is passed to the DataMuse API to retrieve matching rhyming words (and phrases). The API returns matching words (and phrases), in JSON, along with a score parameter for how well each word or phrase rhymes with the noun.  

I've used the [British National Corpus (BNC)](http://www.natcorp.ox.ac.uk/) to source more interesting word pairs for the rhyming pairs. The idea was that the BNC could offer interesting matches that would feel closer to actual Cockney rhyming slang. The BNC is a 100 million word collection representing a cross-section of British English, both spoken and written, from the late twentieth century.

I've extracted all the Noun-Noun bi-gram pairs (or collocations) from the BNC. This data is stored in ```bnc.py``` in the ```/data``` directory of this repo. For each rhyming word returned by the DataMuse API, the script looks for a matched pair within the BNC bi-gram pairs. These matches can then be used to construct the rhyming slang.

If a preferable match can't be found in the BNC bi-grams, the script will look through all of the DataMuse rhyming results. The script will identify if the DataMuse results already contain a word pair and use that instead in order to construct the rhyming slang. If a noun can't be rhymed with, then it will be skipped.  

The script will select the "**best match**" it can find, based on the frequency scores of the BNC bi-grams (frequency of use in modern British English). The script can also run in **random mode** where the frequency scores are ignored and a random match is chosen. You can have some fun watching the different possible rhyming slang constructions being returned each time the script is run in **random mode**.  

### Prerequisites

The script is written in Python 2.7.

Requires the following Python modules installed in order to call the DataMuse Rhyming API and parse its JSON response:

```
import requests
import json
```

The following modules are required for light Natural Language Processing (NLP) tasks:

```
from nltk import word_tokenize, pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
import inflect
```

I've used the WordNet Lemmatizer as opposed to other options (e.g. stemmers such as the PorterStemmer) available in NLTK. You can play around and implement something different by quickly modifying the ```stem()``` function in the script. 

### Installing

Required modules are available from PyPI and can easily be installed as follows:

```
pip install requests, json
pip install nltk, inflect
```

The script also uses a number of pre-installed Python libraries such as ```random``` and also ```itemgetter``` from the ```operator``` library. 

## Running the Script

Usage Example: 

```
>>> python cockneyRhymer.py -b -f ./test/inputText.txt ./test/outputText.txt

>>> python cockneyRhymer.py -b "I don't go south of the river."
>>> river rhymes with liver, cod liver
>>> i don't go south of the cod.

>>> python cockneyRhymer.py -r "You're having a laugh!"
>>> laugh rhymes with graf, stephi graf
>>> you're having a stephi!

>>> python cockneyRhymer.py -r "This car is an old banger."
>>> car rhymes with bar, chocolate bar
>>> banger rhymes with langer, bernhard langer
>>> this chocolate is an old bernhard.
```

The first parameter denotes the type of rhyming pairs the script will select. Options are:

* -r = selects a rhyming pair at random from a list of matched rhyming pairs
* -b = selects best rhyming pair from the list, based on the frequency score within the BNC data

If passing the ```-f``` option as a second parameter the script will expect the following two arguments to contain file paths for an input text file (to be converted to rhyming slang) and output file (to store the rhyming slang output). If this parameter is not passed, the script will expect input in the form of text string, passed as an argument, and prints rhyming slang conversions to stdout. 

## Testing

Here's a short list of famous Cockney rhyming slang.

English | Rhymes with     |	Cockney          | 
:------:|:---------------:|:----------------:|
Feet    | Plates of meat  | Plates           |
Teeth	  | Hampstead Heath | Hampsteads       |
Legs	  | Scotch eggs	    | Scotches         |
Eyes	  | Mince pies	    | Minces           |
Arms	  | Chalk Farms	    | Chalk Farms      |
Hair	  | Barnet Fair	    | Barnet           |
Head	  | Loaf of bread	  | Loaf             |
Face	  | Boat race	      | Boat race        |
Mouth	  | North and south | North and south  |

Here's a sample of alternatives generated by cockneyRhymer.py and after some intitial cleaning of the BNC bi-grams data. 

English | Rhymes with     | cockneyRhymer.py |
:------:|:---------------:|:----------------:|
Feet    | Balance Sheet   | Balances         |
Teeth	  | Edward Heath    | Heaths           |
Legs	  | Easter eggs	    | Easters          |
Eyes	  | Money Supplies  | Monies           |
Arms	  | Burglar alarms  | Burglars         |
Hair	  | Health care	    | Health           |
Head	  | Hospital bed	  | Hospital         |
Face	  | Market place    | Market           |
Mouth	  | **New south**   | **New**          |

Only the final rhyming slang match is a rather wonky one.

"Water Supplies" for "Eyes" was a close second!

Last but not least, my favourite cockneyRhymer.py alternative for the classic "Dog and Bone = Phone".

```
   >>> python cockneyRhymer.py -r "I'll call you on the phone."
   >>> phone rhymes with stone, sharon stone 
   >>> i'll call you on the sharon.
```

Enjoy and Michael Banks for reading!

<p align="center">
  <img src="/doc/rubadubdub.jpg"/>
</p>

## To Do

* The BNC dataset of noun-noun bi-grams still requires some cleaning
* Implement a built in rhyming algorithm to replace the DataMuse API

## Built With

* [Python](http://www.python.org)
* [NLTK](https://www.nltk.org/)
* [Inflect](https://github.com/jazzband/inflect)
* [DataMuse API](https://www.datamuse.com/api/)
* [British National Corpus (BNC)](http://natcorp.ox.ac.uk)

## Authors

* **Andrew Houlbrook** - *Initial work* - [andrewhoulbrook](https://github.com/andrewhoulbrook)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details