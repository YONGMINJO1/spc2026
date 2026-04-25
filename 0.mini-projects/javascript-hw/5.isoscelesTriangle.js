function isoscelesTriangle(lines) {
  for (let i = 1; i <= lines; i++) {
    console.log(' '.repeat(lines - i) + '*'.repeat(i * 2 - 1));
  }
}

isoscelesTriangle(5);
