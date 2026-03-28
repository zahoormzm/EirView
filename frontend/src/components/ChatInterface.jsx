import { Send } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import { streamChat } from '../api';
import useStore from '../store';

export default function ChatInterface({ chatType, userId, title, placeholder, tall = false }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [streaming, setStreaming] = useState(false);
  const scrollRef = useRef(null);
  const { showToast } = useStore();

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages, streaming]);

  const send = async () => {
    if (!input.trim() || streaming) return;
    const userMessage = { role: 'user', content: input };
    const history = [...messages, userMessage];
    setMessages(history);
    setInput('');
    setStreaming(true);
    setMessages((previous) => [...previous, { role: 'assistant', content: '' }]);
    try {
      await streamChat(
        chatType,
        userId,
        userMessage.content,
        messages,
        (chunk) => setMessages((previous) => previous.map((item, index) => index === previous.length - 1 ? { ...item, content: item.content + chunk } : item)),
        (tool) => setMessages((previous) => [...previous, { role: 'tool', content: `${tool.name}: ${JSON.stringify(tool.result)}` }]),
        () => setStreaming(false)
      );
    } catch (error) {
      setStreaming(false);
      showToast(error.message, 'error');
    }
  };

  return (
    <div className={`bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col ${tall ? 'h-[600px]' : 'h-[500px]'}`}>
      <div className="px-4 py-3 border-b border-slate-200 font-semibold text-slate-900">{title}</div>
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4">
        {!messages.length && <div className="text-sm text-slate-500">Start the conversation.</div>}
        {messages.map((message, index) => (
          <div key={`${message.role}-${index}`} className={message.role === 'user' ? 'flex justify-end' : 'flex justify-start'}>
            {message.role === 'tool' ? (
              <div className="bg-amber-50 border border-amber-200 rounded-lg px-3 py-2 text-xs text-amber-700 my-1 max-w-full">{message.content}</div>
            ) : (
              <div className={`${message.role === 'user' ? 'bg-emerald-100 text-emerald-900 rounded-2xl rounded-br-md' : 'bg-white border border-slate-200 text-slate-700 rounded-2xl rounded-bl-md'} px-4 py-2.5 max-w-[75%] text-sm`}>
                {message.content}
              </div>
            )}
          </div>
        ))}
        {streaming && messages[messages.length - 1]?.role !== 'assistant' && (
          <div className="flex justify-start">
            <div className="bg-white border border-slate-200 rounded-2xl rounded-bl-md px-4 py-2.5 flex gap-1">
              <span className="w-2 h-2 bg-slate-400 rounded-full typing-dot" />
              <span className="w-2 h-2 bg-slate-400 rounded-full typing-dot" />
              <span className="w-2 h-2 bg-slate-400 rounded-full typing-dot" />
            </div>
          </div>
        )}
      </div>
      <div className="border-t border-slate-200 p-4 flex gap-2">
        <input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          onKeyDown={(event) => event.key === 'Enter' && send()}
          placeholder={placeholder}
          aria-label={placeholder}
          className="flex-1 border border-slate-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none"
        />
        <button onClick={send} disabled={streaming} aria-label={`Send ${title} message`} className="bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg px-4 py-2 font-medium transition disabled:opacity-60">
          <Send size={16} />
        </button>
      </div>
    </div>
  );
}
