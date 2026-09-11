# Tabellen für Enemy Randomizer

Dieses Verzeichnis enthält automatisch erzeugte Tabellen (JSON), die vom Python-Enemy-Randomizer genutzt werden.

Verwendete Dateien:
- DoS Enemies.txt
- enemy_randomizer.rb

Wie man die Tabellen neu erzeugt:
  python3 experimental/tabellen/generate_tables.py

Die erzeugten Dateien sind:
- enemies.json             -> Liste von Objekten {id, name, requires_overlay, is_spawner}
- resource_intensive.json  -> Liste von Gegnernamen, die als ressourcenintensiv gelten
- boss_list.json           -> Liste von Bossen (IDs oder Namen)

Vorsicht: die Parser sind heuristisch und lesen aus den experimental-Textdateien. Überprüfe die Ergebnisse vor dem Anwenden eines full-swap auf eine ROM-Kopie.
