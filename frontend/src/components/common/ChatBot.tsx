
'use client';

import React, { useState, useRef, useEffect } from 'react';
import { FaRobot, FaTimes, FaPaperPlane } from 'react-icons/fa';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

export default function ChatBot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: 'Hello! 👋 I\'m your trekking assistant. How can I help you today?',
      sender: 'bot',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const quickReplies = [
    'Popular treks',
    'Trek prices',
    'Best season',
    'Booking process',
  ];

  const getBotResponse = (userMessage: string): string => {
    const msg = userMessage.toLowerCase();

    if (msg.includes('popular') || msg.includes('recommend')) {
      return 'Our most popular treks are:\n\n1. Everest Base Camp (12 days) - $1,299\n2. Annapurna Base Camp (7 days) - $699\n3. Mardi Himal (5 days) - $499\n4. Poon Hill (4 days) - $399\n\nWhich one interests you?';
    }

    if (msg.includes('price') || msg.includes('cost')) {
      return 'Our trek prices range from $399 to $2,299 depending on duration and difficulty. Prices include guide, porter, permits, accommodation, and meals. Would you like details about a specific trek?';
    }

    if (msg.includes('season') || msg.includes('when') || msg.includes('time')) {
      return 'The best time for trekking in Nepal is:\n\n🌸 Spring (March-May): Clear views, warm weather, rhododendrons bloom\n🍂 Autumn (September-November): Clearest skies, best visibility\n\nWinter and monsoon are less ideal except for certain treks like Upper Mustang.';
    }

    if (msg.includes('book') || msg.includes('reservation')) {
      return 'Booking is easy! Just:\n1. Choose your trek\n2. Select dates\n3. Fill in details\n4. Make secure payment\n\nWe accept Stripe, Khalti, and eSewa. Need help with booking?';
    }

    if (msg.includes('everest') || msg.includes('ebc')) {
      return 'Everest Base Camp Trek (12 days) - $1,299\n\n✓ Moderate difficulty\n✓ Max altitude: 5,364m\n✓ Best season: Mar-May, Sep-Nov\n✓ Includes permits, guide, porter, meals\n\nView full details or book now?';
    }

    if (msg.includes('annapurna') || msg.includes('abc')) {
      return 'Annapurna Base Camp Trek (7 days) - $699\n\n✓ Moderate difficulty\n✓ Max altitude: 4,130m\n✓ Best season: Mar-May, Sep-Nov\n✓ Spectacular mountain views\n\nInterested in booking?';
    }

    if (msg.includes('hello') || msg.includes('hi')) {
      return 'Hello! 😊 I can help you with:\n\n• Trek recommendations\n• Pricing information\n• Best trekking seasons\n• Booking assistance\n\nWhat would you like to know?';
    }

    return 'Thanks for your message! For detailed information, you can:\n\n1. Browse our treks page\n2. Contact us via WhatsApp: +977 9846958184\n3. Email: info@nepaltrekconnect.com\n\nOr ask me another question!';
  };

  const handleSend = () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: messages.length + 1,
      text: input,
      sender: 'user',
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    // Simulate bot typing and response
    setTimeout(() => {
      const botResponse: Message = {
        id: messages.length + 2,
        text: getBotResponse(input),
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botResponse]);
      setIsTyping(false);
    }, 1500);
  };

  const handleQuickReply = (reply: string) => {
    setInput(reply);
    setTimeout(() => handleSend(), 100);
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 z-40 bg-primary-600 hover:bg-primary-700 text-white rounded-full p-4 shadow-2xl hover:scale-110 transition-all duration-300"
        aria-label="Open chat"
      >
        <FaRobot size={28} />
      </button>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 z-40 w-96 max-w-[calc(100vw-2rem)] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden">
      {/* Header */}
      <div className="bg-primary-600 text-white px-4 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <FaRobot size={24} />
          <div>
            <h3 className="font-semibold">Trek Assistant</h3>
            <p className="text-xs opacity-90">Online now</p>
          </div>
        </div>
        <button
          onClick={() => setIsOpen(false)}
          className="hover:bg-primary-700 rounded-full p-1 transition-colors"
        >
          <FaTimes size={20} />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 p-4 space-y-3 overflow-y-auto max-h-96 bg-gray-50">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] px-4 py-2 rounded-2xl whitespace-pre-line ${
                message.sender === 'user'
                  ? 'bg-primary-600 text-white rounded-br-none'
                  : 'bg-white text-gray-800 rounded-bl-none shadow-sm'
              }`}
            >
              <p className="text-sm">{message.text}</p>
              <p className={`text-xs mt-1 ${message.sender === 'user' ? 'text-primary-100' : 'text-gray-400'}`}>
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </p>
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-white text-gray-800 px-4 py-2 rounded-2xl rounded-bl-none shadow-sm">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Replies */}
      {messages.length === 1 && (
        <div className="px-4 py-2 bg-gray-100 flex flex-wrap gap-2">
          {quickReplies.map((reply) => (
            <button
              key={reply}
              onClick={() => handleQuickReply(reply)}
              className="text-xs bg-white hover:bg-primary-50 text-primary-600 border border-primary-200 px-3 py-1 rounded-full transition-colors"
            >
              {reply}
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="p-3 border-t bg-white">
        <div className="flex items-center space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:border-primary-500 text-sm"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim()}
            className="bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 text-white rounded-full p-2 transition-colors"
          >
            <FaPaperPlane size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}