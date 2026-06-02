from langchain_community.agent_toolkits.load_tools import get_all_tool_names

print('-----load_tools 를 통해 가져올 수 있는 도구-----')
names = sorted(get_all_tool_names())

for name in names:
    print(f"- {name}")

print(f"\n를 {len(name)}개 가 현재 사용가능")