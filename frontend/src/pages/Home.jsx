import { useNavigate } from 'react-router-dom';
import { BrainCircuit, Swords, Trophy } from 'lucide-react';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center py-12 px-4">
      <div className="max-w-3xl text-center space-y-8">
        <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight text-gray-900">
          Trở thành cao thủ Cờ Caro với <br className="hidden md:block"/>
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-emerald-500">
            AI Siêu Trí Tuệ
          </span>
        </h1>
        
        <p className="text-xl text-gray-600 leading-relaxed max-w-2xl mx-auto">
          Sản phẩm cuối kỳ môn Trí tuệ Nhân tạo. 
          Hãy thử sức với thuật toán Minimax kết hợp Alpha-Beta hoặc chơi cùng bạn bè!
        </p>

        <button 
          onClick={() => navigate('/setup')}
          className="mt-8 px-8 py-4 bg-indigo-600 text-white rounded-full font-bold text-lg hover:bg-indigo-700 hover:shadow-xl hover:-translate-y-1 transition-all duration-200"
        >
          Chơi Ngay
        </button>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16 text-left">
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-indigo-100 text-indigo-600 rounded-xl flex items-center justify-center mb-4">
              <BrainCircuit size={24} />
            </div>
            <h3 className="text-xl font-bold mb-2">AI Thông Minh</h3>
            <p className="text-gray-600">Ba mức độ khó dựa trên các mẫu đánh giá và cây tìm kiếm Minimax.</p>
          </div>
          
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-emerald-100 text-emerald-600 rounded-xl flex items-center justify-center mb-4">
              <Swords size={24} />
            </div>
            <h3 className="text-xl font-bold mb-2">Nhiều Chế Độ</h3>
            <p className="text-gray-600">Chế độ Người vs Máy, Người vs Người, hoặc xem Máy vs Máy thi đấu.</p>
          </div>
          
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-amber-100 text-amber-600 rounded-xl flex items-center justify-center mb-4">
              <Trophy size={24} />
            </div>
            <h3 className="text-xl font-bold mb-2">Phân Tích Chi Tiết</h3>
            <p className="text-gray-600">Xem chỉ số theo thời gian thực: điểm đánh giá, độ sâu tìm kiếm, số nút đã xét.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
