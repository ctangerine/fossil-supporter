import os
import sys
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from typing import Optional

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from core.config import settings 

class Fossil(BaseModel):
    species: Optional[str] = Field(None, description="Tên loài của hóa thạch, nêu tên đầy đủ, tên trong tiếng Việt, họ, bộ ..., chỉ trả về khi nội dung liên quan")
    era: Optional[str] = Field(None, description="Thời đại địa chất của hóa thạch, nêu tên thời đại trong khoa học, trong tiếng Việt (ví dụ: kỷ ...), chỉ trả về khi nội dung liên quan")
    biological_features: Optional[str] = Field(None, description="Đặc điểm sinh học chi tiết của hóa thạch, phải trả lời chi tiết, chỉ trả về khi nội dung liên quan")
    science_significance: Optional[str] = Field(None, description="Ý nghĩa khoa học của hóa thạch, nói thạt chi tiết, chỉ trả về khi nội dung liên quan")
    confuse_with: Optional[str] = Field(None, description="Tên các loài khác có thể bị nhầm lẫn với hóa thạch này, chỉ trả về khi nội dung liên quan")
    fossil_related: Optional[bool] = Field(None, description="Nội dung có liên quan đến hóa thạch hay không; chỉ trả về khi không liên quan")
    refuse_message: Optional[str] = Field(None, description="Phản hồi cho người dùng nếu nội dung không liên quan đến hóa thạch; chỉ trả về khi không liên quan")


class Chatbot:
    def __init__(self):
        self.model = init_chat_model(
            "gemini-2.0-flash", 
            model_provider="google_genai",
            google_api_key="AIzaSyCnZQ9fBebxFrzYT9bgmba8OTQYqcfx1NY"
        )

        self.model = self.model.with_structured_output(Fossil)

        self.system_message = SystemMessage(
            content=(
                "Bạn là một chuyên gia hóa thạch với kiến thức sâu rộng về sinh vật cổ đại, "
                "các loài hóa thạch và quá trình hóa thạch. Bạn chỉ chuyên phân tích hình ảnh "
                "hóa thạch được cung cấp và đưa ra kết quả thật chi tiết về loài, thời đại địa chất, "
                "đặc điểm sinh học và ý nghĩa khoa học. Bạn sẽ từ chối trả lời bất kỳ câu hỏi nào "
                "không liên quan đến hóa thạch hoặc phân tích những hình ảnh không phải là hóa thạch.\n\n"
                "Yêu cầu phản hồi chi tiết như sau:\n"
                "- species: viết thành câu đầy đủ, thân thiện, ví dụ: 'Thuộc loài Ammonitida, hay còn gọi là cúc đá...'. Có thể bổ sung thông tin về họ, bộ, phân lớp.\n"
                "- era: nêu tên đại địa chất (ví dụ: Đại Trung Sinh - Mesozoic Era), kèm khoảng thời gian (ví dụ: cách đây khoảng 250–66 triệu năm), cụ thể thuộc về kỷ nào và đặc điểm của kỷ đó hoặc thông tin nổi bật, hoặc sự kiện địa chất/sinh học quan trọng của từng kỷ.\n"
                "- biological_features: mô tả chi tiết hình dạng, cấu tạo, chức năng,(ví dụ: buồng khí, vỏ), tập tính sinh học giả định của loài đã xác định (không đề cập đến các thông tin trong ảnh hóa thạch)... Độ dài ít nhất vài câu.\n"
                "- science_significance: giải thích sâu về ý nghĩa trong nghiên cứu địa tầng, cổ sinh học, tiến hóa. Nêu ví dụ cụ thể như 'giúp xác định niên đại tương đối của các lớp đá kỷ Jura…'. Độ dài ít nhất vài câu.\n"
                "- confuse_with: liệt kê tên các loài khác có thể bị nhầm lẫn với hóa thạch này về mặt hình ảnh (mức độ không chắc chắn trong nhận diện), lí do có thể gây nhầm lẫn. Chỉ trả về khi nội dung liên quan.\n"
                "Phong cách viết và văn phong phải khoa học, nghiêm túc, đầy thông tin.\n\n"
                "Nếu hình ảnh liên quan đến hóa thạch, hãy trả về object gồm:\n"
                "- species, era, biological_features, science_significance (các trường này phải có giá trị)\n"
                "Nếu hình ảnh KHÔNG liên quan đến hóa thạch, trả về object chỉ gồm:\n"
                "- fossil_related: false\n"
                "- refuse_message: '...' (giải thích ngắn gọn lý do từ chối)\n"
                "Không trả về các trường species, era, biological_features, science_significance khi nội dung không liên quan."
            )
        )

    # def ask(self, user_input: str):
    #     messages = [
    #         self.system_message,
    #         HumanMessage(content=user_input)
    #     ]
    #     for chunk in self.model.stream(messages):
    #         yield chunk

    def ask(self, image_path: str):
        import base64
        
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode()
        
        messages = [
            self.system_message,
            HumanMessage(content=[
                {"type": "text", "text": "Phân tích hình ảnh hóa thạch."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
            ])
        ]

        response = self.model.invoke(messages)
        return response
    
# Example usage:
chatbot = Chatbot()
response = chatbot.ask("C:\\RIKAI\\tmp_project\\R.png")

print(response)