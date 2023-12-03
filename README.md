# Manga Scrapper

## Deprecated move to <a href="https://github.com/nothing2512/manga">here</a>

### Setup
`pip install -r requirements.txt`

### Sites Available
<ul>
    <li><a href="https://komiku.id">Komiku</a></li>
    <li><a href="https://klikmanga.com">Klikmanga</a></li>
</ul>

### Manga Status
0: Archieved<br>
1: Basic<br>
6: Ended<br>
21: Paused<br>

### Usage

Add Manga<br>
`python add.py <link>` <br>
Example<br>
`python add.py https://komiku.com/manga/boruto-id` <br><br>

Check updated manga<br>
basic: `python check.py` <br>
check paused and unpaused manga: `python check.py --all` <br><br>

Download updated manga<br>
`python download.py` <br><br>

Reset Manga<br>
`python reset.py <id>` <br>
Example<br>
`python reset.py 1` <br><br>

Archieve Manga<br>
`python archieve.py <id>` <br>
Example<br>
`python archieve.py 1` <br><br>

Unarchieve Manga<br>
`python unarchieve.py <id>` <br>
Example<br>
`python unarchieve.py 1` <br><br>

Delete Manga<br>
`python delete.py <id>` <br>
Example<br>
`python delete.py 1` <br><br>
