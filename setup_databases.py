"""
Database setup script for creating mock databases.
Creates sample databases for baseball stats, Olympics, and other data.
"""
import sqlite3
import os


def create_baseball_database(db_path):
    """Create a mock baseball statistics database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create players table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            team TEXT,
            position TEXT,
            birth_year INTEGER
        )
    """)
    
    # Create statistics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS statistics (
            stat_id INTEGER PRIMARY KEY,
            player_id INTEGER,
            year INTEGER,
            games_played INTEGER,
            at_bats INTEGER,
            hits INTEGER,
            home_runs INTEGER,
            walks INTEGER,
            strikeouts INTEGER,
            batting_average REAL,
            FOREIGN KEY (player_id) REFERENCES players(player_id)
        )
    """)
    
    # Create jersey numbers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jersey_numbers (
            id INTEGER PRIMARY KEY,
            player_id INTEGER,
            jersey_number INTEGER,
            year INTEGER,
            FOREIGN KEY (player_id) REFERENCES players(player_id)
        )
    """)
    
    # Insert sample players (Yankees theme)
    players = [
        (1, "Derek Jeter", "Yankees", "SS", 1974),
        (2, "Babe Ruth", "Yankees", "OF", 1895),
        (3, "Lou Gehrig", "Yankees", "1B", 1903),
        (4, "Mickey Mantle", "Yankees", "OF", 1931),
        (5, "Yogi Berra", "Yankees", "C", 1925),
        (6, "Joe DiMaggio", "Yankees", "OF", 1914),
        (7, "Mariano Rivera", "Yankees", "P", 1969),
        (8, "Alex Rodriguez", "Yankees", "3B", 1975),
        (9, "Don Mattingly", "Yankees", "1B", 1961),
        (10, "Reggie Jackson", "Yankees", "OF", 1946),
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO players (player_id, name, team, position, birth_year)
        VALUES (?, ?, ?, ?, ?)
    """, players)
    
    # Insert sample statistics
    statistics = [
        # Derek Jeter - high walks
        (1, 1, 2000, 148, 593, 201, 15, 68, 99, 0.339),
        (2, 1, 2005, 159, 654, 202, 19, 77, 117, 0.309),
        (3, 1, 2009, 153, 634, 212, 18, 72, 100, 0.334),
        # Babe Ruth
        (4, 2, 1927, 151, 540, 192, 60, 137, 89, 0.356),
        (5, 2, 1923, 152, 522, 205, 41, 170, 93, 0.393),
        # Lou Gehrig
        (6, 3, 1927, 155, 584, 218, 47, 109, 84, 0.373),
        (7, 3, 1930, 154, 581, 220, 41, 101, 63, 0.379),
        # Mickey Mantle
        (8, 4, 1956, 150, 533, 188, 52, 112, 99, 0.353),
        (9, 4, 1961, 153, 514, 163, 54, 126, 112, 0.317),
        # Others
        (10, 5, 1950, 151, 597, 192, 28, 55, 12, 0.322),
        (11, 6, 1941, 139, 541, 193, 30, 76, 13, 0.357),
        (12, 7, 2004, 74, 0, 0, 0, 6, 0, 0.000),  # Pitcher
        (13, 8, 2007, 158, 583, 183, 54, 95, 120, 0.314),
        (14, 9, 1985, 159, 652, 211, 35, 56, 41, 0.324),
        (15, 10, 1977, 146, 525, 150, 32, 74, 133, 0.286),
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO statistics 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, statistics)
    
    # Insert jersey numbers
    jerseys = [
        (1, 1, 2, 1996),   # Jeter #2
        (2, 2, 3, 1920),   # Ruth #3
        (3, 3, 4, 1925),   # Gehrig #4
        (4, 4, 7, 1951),   # Mantle #7
        (5, 5, 8, 1946),   # Berra #8
        (6, 6, 5, 1936),   # DiMaggio #5
        (7, 7, 42, 1995),  # Rivera #42
        (8, 8, 13, 2004),  # A-Rod #13
        (9, 9, 23, 1982),  # Mattingly #23
        (10, 10, 44, 1977), # Reggie #44
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO jersey_numbers 
        VALUES (?, ?, ?, ?)
    """, jerseys)
    
    conn.commit()
    conn.close()
    print(f"✓ Baseball database created: {db_path}")


def create_olympics_database(db_path):
    """Create a mock Olympics database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create countries table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            country_id INTEGER PRIMARY KEY,
            country_name TEXT NOT NULL,
            country_code TEXT,
            exists_today INTEGER  -- 1 if exists, 0 if historical
        )
    """)
    
    # Create olympics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS olympics (
            olympic_id INTEGER PRIMARY KEY,
            year INTEGER,
            season TEXT,
            city TEXT,
            country_id INTEGER,
            FOREIGN KEY (country_id) REFERENCES countries(country_id)
        )
    """)
    
    # Create athletes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS athletes (
            athlete_id INTEGER PRIMARY KEY,
            country_id INTEGER,
            name TEXT,
            sport TEXT,
            medals INTEGER,
            FOREIGN KEY (country_id) REFERENCES countries(country_id)
        )
    """)
    
    # Insert countries (including historical ones)
    countries = [
        (1, "United States", "USA", 1),
        (2, "China", "CHN", 1),
        (3, "Russia", "RUS", 1),
        (4, "Germany", "GER", 1),
        (5, "Great Britain", "GBR", 1),
        (6, "Japan", "JPN", 1),
        (7, "Australia", "AUS", 1),
        (8, "France", "FRA", 1),
        (9, "East Germany", "GDR", 0),  # Historical - no longer exists
        (10, "Soviet Union", "URS", 0),  # Historical - no longer exists
        (11, "Yugoslavia", "YUG", 0),    # Historical - no longer exists
        (12, "Czechoslovakia", "TCH", 0), # Historical - no longer exists
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO countries VALUES (?, ?, ?, ?)
    """, countries)
    
    # Insert Olympics
    olympics = [
        (1, 2020, "Summer", "Tokyo", 6),
        (2, 2016, "Summer", "Rio", 1),
        (3, 2012, "Summer", "London", 5),
        (4, 2008, "Summer", "Beijing", 2),
        (5, 2004, "Summer", "Athens", 8),
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO olympics VALUES (?, ?, ?, ?, ?)
    """, olympics)
    
    # Insert athletes (Tokyo 2020 - varying team sizes)
    athletes = [
        # USA - 613 athletes
        *[(None, 1, f"USA Athlete {i}", "Various", 0) for i in range(1, 614)],
        # China - 431 athletes
        *[(None, 2, f"China Athlete {i}", "Various", 0) for i in range(1, 432)],
        # ROC (Russia) - 335 athletes
        *[(None, 3, f"ROC Athlete {i}", "Various", 0) for i in range(1, 336)],
        # Great Britain - 376 athletes
        *[(None, 5, f"GB Athlete {i}", "Various", 0) for i in range(1, 377)],
        # Japan - 583 athletes
        *[(None, 6, f"Japan Athlete {i}", "Various", 0) for i in range(1, 584)],
        # Australia - 472 athletes
        *[(None, 7, f"AUS Athlete {i}", "Various", 0) for i in range(1, 473)],
    ]
    
    cursor.executemany("""
        INSERT INTO athletes (athlete_id, country_id, name, sport, medals)
        VALUES (?, ?, ?, ?, ?)
    """, athletes)
    
    conn.commit()
    conn.close()
    print(f"✓ Olympics database created: {db_path}")


def create_competitions_database(db_path):
    """Create a mock competition/awards database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create competitions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitions (
            competition_id INTEGER PRIMARY KEY,
            name TEXT,
            year INTEGER,
            category TEXT
        )
    """)
    
    # Create winners table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS winners (
            winner_id INTEGER PRIMARY KEY,
            competition_id INTEGER,
            winner_name TEXT,
            country_id INTEGER,
            year INTEGER,
            FOREIGN KEY (competition_id) REFERENCES competitions(competition_id)
        )
    """)
    
    # Create historical countries reference
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historical_countries (
            country_id INTEGER PRIMARY KEY,
            country_name TEXT,
            existed_from INTEGER,
            existed_to INTEGER
        )
    """)
    
    # Insert sample data
    competitions = [
        (1, "International Math Olympiad", 1990, "Mathematics"),
        (2, "Chess World Championship", 1985, "Chess"),
        (3, "Science Fair International", 1991, "Science"),
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO competitions VALUES (?, ?, ?, ?)
    """, competitions)
    
    # Winners from countries that no longer exist
    winners = [
        (1, 1, "Ivan Petrov", 10, 1990),  # Soviet Union
        (2, 2, "Petra Novak", 12, 1985),  # Czechoslovakia
        (3, 3, "Josip Horvat", 11, 1991), # Yugoslavia
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO winners VALUES (?, ?, ?, ?, ?)
    """, winners)
    
    # Historical countries
    historical = [
        (10, "Soviet Union", 1922, 1991),
        (11, "Yugoslavia", 1918, 1992),
        (12, "Czechoslovakia", 1918, 1993),
        (13, "East Germany", 1949, 1990),
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO historical_countries VALUES (?, ?, ?, ?)
    """, historical)
    
    conn.commit()
    conn.close()
    print(f"✓ Competitions database created: {db_path}")


if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    print("Creating mock databases...")
    print("=" * 60)
    
    # Create all databases
    create_baseball_database("data/baseball.db")
    create_olympics_database("data/olympics.db")
    create_competitions_database("data/competitions.db")
    
    print("=" * 60)
    print("✅ All databases created successfully!")
    print("\nDatabases created:")
    print("  - data/baseball.db (Yankees players, stats, jersey numbers)")
    print("  - data/olympics.db (Countries, athletes, Olympics data)")
    print("  - data/competitions.db (Historical competitions and winners)")
