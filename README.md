# Color_Music_Exp
## **Stair case method in psychopy for Measuring Effects**



#### Requirements & Execution

---

***Requirements***

→ Navigate to the folder. and run the following code through terminal/commandprompt.

```bash
pip install -r requirements.txt
```

→ Create two separate directories. `dictionary_bw` & `dictionary_color` & run the following command ( ***If Linux/Mac Terminal*** ) 

```bash
mkdir dictionary_bw && cp createDictionary_bw.py ./dictionary_bw
```

```bash
mkdir dictionary_color && cp createDictionary_color.py ./dictionary_color
```

then, 

```bash
cp runexp.py ./dictionary_bw
```

```bash
cp runexp.py ./dictionary_color
```

(or)

***If Windows***

→ Create and copy the files into the respected dictionary folders ( that are created ) manually. 

→ copy `runexp.py` to both dictionary folders.

---

***Execution*** - Using Standalone Psychopy Application.

→ Open psychopy ( if windows, run as administrator)

→ Click file → open → Navigate to the `runexp.py` in either of those of folders depending on the experiment that you want to run (`dictionary_bw` or `dictionary_color`).  

→ Click on `run experiment button` on the top. 

---

***Running under a Conda Environment.*** 

First, run

```bash
conda activate your-environment
```

then, establish all the requirements by following the above process. 

***Creating New Environment with the Following***

Python 3.8, (3.10 has posed issues on some machines)

Create a conda environment with: `requirements.txt`
---



