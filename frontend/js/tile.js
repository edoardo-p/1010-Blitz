class Tile {
  constructor(colour=0, empty=true) {
    this.colour = colour;
    this.empty = empty;
  }

  update(colour) {
    this.colour = colour;
    if (colour === 0) {
      this.empty = true;
    } else {
      this.empty = false;
    }
  }
}
