// =====================
// 1. 이름 데이터
// =====================
const names = [
  "김민준", "이서연",
  "박지호", "최수아", "정우진", "한예린",
  "윤도현", "임채원", "강민서", "오준혁", "신다은",
  "류성호", "백지수", "송민재", "전하늘", "노을찬",
  "문서준", "안소희", "배태양",
  "홍길동", "성춘향", "변학도", "이몽룡", "춘삼이",
  "나그네", "바람돌", "하늘별", "구름달", "노을빛",
  "새벽이"
];

// 자리 ID 순서 (빈칸 제외)
const seatIds = [
  "seat-a1", "seat-a2", "seat-a3", "seat-a4",
  "seat-a5", "seat-a6",
  "seat-b1", "seat-b2", "seat-b3", "seat-b4",
  "seat-b5", "seat-b6", "seat-b7", "seat-b8",
  "seat-b9", "seat-b10", "seat-b11", "seat-b12",
  "seat-b13", "seat-b14",
  "seat-d1", "seat-d2", "seat-d3", "seat-d4",
  "seat-d5", "seat-d6", "seat-d7", "seat-d8",
  "seat-d9", "seat-d10"
];

// =====================
// 2. 상태 관리
// =====================
let selectedName = null;

// =====================
// 3. 이름 패널 채우기
// =====================
function renderNamePanel() {
  const nameList = document.getElementById("name-list");
  nameList.innerHTML = "";

  names.forEach(function(name) {
    const card = document.createElement("div");
    card.className = "name-card";
    card.textContent = name;
    card.onclick = function() {
      selectName(name, card);
    };
    nameList.appendChild(card);
  });
}

// =====================
// 4. 이름 선택
// =====================
function selectName(name, card) {
  if (card.classList.contains("placed")) return;

  document.querySelectorAll(".name-card").forEach(function(c) {
    c.classList.remove("selected");
  });

  if (selectedName === name) {
    selectedName = null;
    return;
  }

  selectedName = name;
  card.classList.add("selected");
}

// =====================
// 5. 자리에 이름 표시
// =====================
function renderSeats(nameList) {
  seatIds.forEach(function(id, i) {
    const seat = document.getElementById(id);
    if (seat) {
      seat.textContent = nameList[i] || "";
      seat.classList.remove("occupied");
    }
  });
}

// =====================
// 6. 자리에 이름 배치
// =====================
function placeName(seatEl) {

  // 이미 이름 있는 자리 클릭 → 이름 제거
  if (seatEl.textContent !== "") {
    const removedName = seatEl.textContent;

    // 자리 비우기
    seatEl.textContent = "";
    seatEl.classList.remove("occupied");

    // 패널에서 해당 이름 다시 활성화
    document.querySelectorAll(".name-card").forEach(function(c) {
      if (c.textContent === removedName) {
        c.classList.remove("placed");
      }
    });
    return;
  }

  // 선택된 이름 없으면 무시
  if (!selectedName) return;

  // 자리에 이름 배치
  seatEl.textContent = selectedName;
  seatEl.classList.add("occupied");

  // 패널에서 배치완료 표시
  document.querySelectorAll(".name-card").forEach(function(c) {
    if (c.textContent === selectedName) {
      c.classList.remove("selected");
      c.classList.add("placed");
    }
  });

  selectedName = null;
}

// =====================
// 7. 랜덤 셔플
// =====================
function shuffleSeats() {
  const shuffled = [...names];

  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const temp = shuffled[i];
    shuffled[i] = shuffled[j];
    shuffled[j] = temp;
  }

  renderSeats(shuffled);

  document.querySelectorAll(".name-card").forEach(function(c) {
    c.classList.remove("selected");
    c.classList.add("placed");
  });
  selectedName = null;
}

// =====================
// 8. 초기화
// =====================
function resetSeats() {
  seatIds.forEach(function(id) {
    const seat = document.getElementById(id);
    if (seat) {
      seat.textContent = "";
      seat.classList.remove("occupied");
    }
  });
  selectedName = null;
  renderNamePanel();
}

// =====================
// 9. 페이지 로드
// =====================
renderSeats([]);
renderNamePanel();