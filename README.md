
# Python Unittest Practice

Dieses Repository wurde als Implementierungsübung für die Softwarearchitektur erstellt, wobei der Fokus auf dem Ordner **"Architecture"** liegt. Ziel der Implementierung ist es, grundlegende Prinzipien der Architektur zu erlernen und anzuwenden. Darüber hinaus dient das Projekt als Plattform, um die Praxis des Unit-Testings zu vertiefen und zu üben.

## Tests ausführen

Um die Tests auszuführen, kann der folgende Befehl verwendet werden:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Erklärung des Befehls:
- `-s tests`: Gibt den Ordner an, in dem nach Tests gesucht werden soll (in diesem Fall der Ordner `tests`).
- `-p "test_*.py"`: Sucht nach allen Dateien, die mit `test_` beginnen und die Endung `.py` haben.
- `-v`: Aktiviert die ausführliche Ausgabe der Testergebnisse.

## Ziel des Projekts

Das Projekt bietet eine strukturierte Umgebung, um sowohl die Implementierung als auch das Testen von Softwarekomponenten zu üben. Es fördert ein besseres Verständnis für:
- Die Bedeutung von sauberem und wartbarem Code.
- Die Rolle von zuverlässigen Unit-Tests in der Softwareentwicklung.

Dieses Repository ist ideal, um praktische Erfahrungen in der Softwarearchitektur und im Testen zu sammeln.
