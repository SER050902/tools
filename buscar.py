import os
import platform

def search_keyword_in_file(file_path, keyword):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if keyword in line:
                    return True
    except Exception:
        pass
    return False

def search_all_dirs(keyword, extensions=None):
    system = platform.system()
    if system == 'Windows':
        drives = [f"{chr(letter)}:\\" for letter in range(65, 91) if os.path.exists(f"{chr(letter)}:\\")]
    else:
        drives = ['/']  # Linux/Mac

    matched_files = []

    for drive in drives:
        print(f"🔍 正在搜索磁盘: {drive}")
        for root, _, files in os.walk(drive, topdown=True):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    if extensions:
                        if not any(name.lower().endswith(ext) for ext in extensions):
                            continue
                    if search_keyword_in_file(file_path, keyword):
                        matched_files.append(file_path)
                        print(f"✅ 匹配：{file_path}")
                except Exception:
                    continue  # 跳过无权限/坏文件
    return matched_files

def main():
    print("🔍 全盘关键字搜索器")

    keyword = input("🔑 输入要搜索的关键字: ").strip()
    if not keyword:
        print("❌ 关键字不能为空")
        return

    ext_input = input("📂 限定扩展名？（用逗号分隔，如 .log,.txt ，留空为全部）: ").strip()
    extensions = [e.strip().lower() for e in ext_input.split(",") if e.strip()] if ext_input else None

    results = search_all_dirs(keyword, extensions)

    print(f"\n📊 搜索完成，共找到 {len(results)} 个包含“{keyword}”的文件")

    save = input("💾 是否保存结果到 all_results.txt？(y/n): ").strip().lower()
    if save == 'y':
        with open("all_results.txt", "w", encoding="utf-8") as f:
            for path in results:
                f.write(path + "\n")
        print("✅ 结果已保存为 all_results.txt")

if __name__ == "__main__":
    main()
