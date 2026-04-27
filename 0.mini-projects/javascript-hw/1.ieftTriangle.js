function ieftTriangle(lines) {
  for (let i = 1; i <= lines; i++) {
    console.log('*'.repeat(i));
  }
}

ieftTriangle(5); // 결과를 보기 위해 함수 사용

// 화살표 함수로 변경
const ieftTriangleArrow = (lines) => {for (let i=1; i <= lines; i++) { 
  console.log('*'.repeat(i))};
}

ieftTriangleArrow(5);