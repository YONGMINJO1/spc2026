function inverRigthTriangle(lines) {
  for (let i = 5; i >= 1; i--) {
    console.log(' '.repeat(lines - i) + '*'.repeat(i));
  }
}

inverRigthTriangle(5);
