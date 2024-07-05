class Column:
  def __init__(self, name: str, values: list[int]):
    self.name = name
    self.values = values

if __name__ == "__main__":
  c = Column("Sample Column", [1, 2, 3, 4, 5])
  print(f"Column Name: {c.name}")
  print(f"Column Values: {c.values}")