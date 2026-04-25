function invertedLeftTriangle(lines) {
  for (let i = 5; i >= lines; i--) {
    console.log('*'.repeat(i));
  }
}

invertedLeftTriangle(1);
