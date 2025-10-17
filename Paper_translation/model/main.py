from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, StoppingCriteria, StoppingCriteriaList
import pandas as pd

model_name = "VietAI/envit5-translation"  # hoặc "VietAI/vit5-translation" nếu muốn bản nhỏ hơn
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

class StopOnString(StoppingCriteria):
    def __init__(self, stop_str, tokenizer):
        self.stop_str = stop_str
        self.tokenizer = tokenizer
        self.buffer = ""

    def __call__(self, input_ids, scores, **kwargs):
        # Decode token mới nhất và nối vào buffer
        self.buffer = self.tokenizer.decode(input_ids[0], skip_special_tokens=True)
        return self.stop_str in self.buffer
stop_criteria = StoppingCriteriaList([StopOnString("###", tokenizer)])

def model_translate(content, max_len):
    # Tokenize
    inputs = tokenizer(content, return_tensors="pt")
    # Generate
    outputs = model.generate(**inputs, max_length= max_len, stopping_criteria=stop_criteria)
    # Decode
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
def check_title(content):
    return content.split(".")[0]

def menu():
    print("1. Chạy dịch toàn bộ và đưa ra file")
    print("2. Đưa ra demo")
    print("0. Thoát")

def main():
    url_list = pd.read_csv("../data/contentSum.csv")
    while True:
        menu()
        choice = str(input("Nhập lựa chọn: "))
        if choice == "1":
            content_list_vn = []
            title_list_vn = []
            for i in range(len(url_list.iloc[:,0]) - 1):
                content_list_vn.append(model_translate(url_list.iloc[i,3], int(len(url_list.iloc[i,3]) * 1.5)))
                title_list_vn.append(check_title(model_translate(url_list.iloc[i,1], int(len(url_list.iloc[i,1])*1.5))))
                print(f"Xong file thứ {i}")
            file = pd.DataFrame({
                "Tiêu đề": title_list_vn,
                "Nội dung": content_list_vn
            })
            file.to_csv("../data/contentFinal.csv", index=False)
        if choice == "2":
            url = pd.read_csv("../data/contentFinal.csv")
            print(f"Số bài báo: (1 - {len(url.iloc[:,0])}) hoặc nhập 0 để thoát")
            paper_no = int(input("Chọn số: "))
            if paper_no != 0:
                if paper_no > 0 or paper_no <= len(url.iloc[:,0]):
                    print(url.iloc[paper_no - 1, 0], "\n", url.iloc[paper_no - 1, 1])
                else:
                    print(f"Lựa chọn phải từ: (1 - {len(url.iloc[:,0])}")
        else:
            break

if __name__ == "__main__":
    ascii_art = r"""
        ██████╗ ███████╗██╗   ██╗ ██████╗ ██╗      █████╗ ███╗   ██╗██████╗ 
        ██╔══██╗██╔════╝██║   ██║██╔═══██╗██║     ██╔══██╗████╗  ██║██╔══██╗
        ██████╔╝█████╗  ██║   ██║██║   ██║██║     ███████║██╔██╗ ██║██║  ██║
        ██╔══██╗██╔══╝  ██║   ██║██║   ██║██║     ██╔══██║██║╚██╗██║██║  ██║
        ██║  ██║███████╗╚██████╔╝╚██████╔╝███████╗██║  ██║██║ ╚████║██████╔╝
        ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ 
        """
    print(ascii_art)
    main()
