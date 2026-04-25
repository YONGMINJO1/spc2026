function diamond(lines) {
  for (let i = 1; i <= lines; i++) {
    console.log(' '.repeat(lines - i) + '*'.repeat(i * 2 - 1));
  }
  for (let i = 1; i < lines; i++) {
    console.log(' '.repeat(i) + '*'.repeat((lines - 1) * 2 - (i * 2 - 1)));
  }
}

diamond(5);
