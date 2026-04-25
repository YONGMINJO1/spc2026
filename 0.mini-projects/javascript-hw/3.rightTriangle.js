function rightTriangle(lines) {
  for (let i = 1; i <= lines; i++) {
    console.log(' '.repeat(lines - i) + '*'.repeat(i));
  }
}

rightTriangle(5);
