"use client"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { Users, Trophy, MessageCircle, Home, Send } from "lucide-react"

export function GroupsScreen() {
  const [activeGroup, setActiveGroup] = useState<string | null>(null)
  const [message, setMessage] = useState("")
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: "RAMbot",
      content: "How was the event and did you meet a lot people during the event?",
      time: "2m ago",
      isBot: true,
    },
    {
      id: 2,
      sender: "Alex",
      content: "It was great!",
      time: "1m ago",
      isUser: true,
    },
    {
      id: 3,
      sender: "VINCE",
      content: "Can I ask how was the place?",
      time: "1m ago",
      isUser: false,
    },
    {
      id: 4,
      sender: "Alex",
      content: "I hope I can come again",
      time: "30s ago",
      isUser: true,
    },
    {
      id: 5,
      sender: "MARWIN",
      content: "Yes, and you can invite some of your friends next time!",
      time: "20s ago",
      isUser: false,
    },
    {
      id: 6,
      sender: "Alex",
      content: "YEY!! Thank you again",
      time: "10s ago",
      isUser: true,
    },
  ])

  const router = useRouter()

  const groups = [
    {
      name: "DONGMINATION",
      members: "30+ Rams Online",
      avatars: ["D", "O", "N", "G"],
      active: true,
    },
    {
      name: "AI Innovators",
      members: "4/6 Rams",
      avatars: ["A", "I"],
      active: false,
    },
  ]

  const sendMessage = () => {
    if (message.trim()) {
      const newMessage = {
        id: messages.length + 1,
        sender: "Alex",
        content: message,
        time: "now",
        isUser: true,
      }
      setMessages([...messages, newMessage])
      setMessage("")
    }
  }

  if (activeGroup) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col">
        {/* Chat Header */}
        <div className="bg-white border-b p-4">
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="sm" onClick={() => setActiveGroup(null)}>
              ←
            </Button>
            <div>
              <h2 className="font-bold text-lg">DONGMINATION</h2>
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Users className="w-4 h-4" />
                <span>30+ Rams Online</span>
              </div>
            </div>
          </div>
          <div className="flex -space-x-1 mt-2">
            {["D", "O", "N", "G"].map((letter, i) => (
              <div
                key={i}
                className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium text-white ${
                  ["bg-gray-400", "bg-gray-500", "bg-gray-600", "bg-gray-700"][i]
                }`}
              >
                {letter}
              </div>
            ))}
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 p-4 space-y-4 overflow-y-auto">
          {messages.map((msg) => (
            <div key={msg.id} className={`flex ${msg.isUser ? "justify-end" : "justify-start"}`}>
              <div className="max-w-xs">
                {!msg.isUser && !msg.isBot && (
                  <div className="text-xs font-semibold text-gray-600 mb-1">{msg.sender}</div>
                )}
                <div
                  className={`p-3 rounded-lg ${
                    msg.isUser
                      ? "bg-blue-600 text-white"
                      : msg.isBot
                        ? "bg-yellow-400 text-black"
                        : "bg-yellow-400 text-black"
                  }`}
                >
                  {msg.content}
                </div>
                <div className="text-xs text-gray-500 mt-1">{msg.time}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Message Input */}
        <div className="bg-white border-t p-4">
          <div className="flex gap-2">
            <Input
              placeholder="Type a message..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && sendMessage()}
              className="flex-1"
            />
            <Button onClick={sendMessage} size="sm" className="bg-gray-600 hover:bg-gray-700">
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </div>

        {/* Bottom Navigation */}
        <div className="bg-yellow-400 p-2">
          <div className="flex justify-around items-center">
            <Button
              variant="ghost"
              size="sm"
              className="flex flex-col items-center gap-1 text-black"
              onClick={() => router.push("/dashboard")}
            >
              <Home className="w-5 h-5" />
              <span className="text-xs">HOME</span>
            </Button>
            <Button variant="ghost" size="sm" className="flex flex-col items-center gap-1 text-black">
              <Users className="w-5 h-5" />
              <span className="text-xs">GROUPS</span>
            </Button>
            <Button
              variant="ghost"
              size="sm"
              className="flex flex-col items-center gap-1 text-black"
              onClick={() => router.push("/leaderboard")}
            >
              <Trophy className="w-5 h-5" />
              <span className="text-xs">BOARD</span>
            </Button>
            <Button variant="ghost" size="sm" className="flex flex-col items-center gap-1 text-black">
              <MessageCircle className="w-5 h-5" />
              <span className="text-xs">PROFILE</span>
            </Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-blue-900 text-white p-4 text-center">
        <div className="flex items-center justify-center gap-2 mb-2">
          <span>👋</span>
          <span className="font-semibold">Hi, Alex!</span>
        </div>
        <div className="text-sm opacity-90">Your first round starts in 7 mins</div>
      </div>

      <div className="p-4 space-y-4">
        {/* Active Groups */}
        <div className="space-y-3">
          {groups.map((group, index) => (
            <Card key={index} className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex -space-x-1">
                    {group.avatars.map((avatar, i) => (
                      <div
                        key={i}
                        className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium text-white ${
                          ["bg-pink-400", "bg-blue-400", "bg-green-400", "bg-purple-400"][i]
                        }`}
                      >
                        {avatar}
                      </div>
                    ))}
                  </div>
                  <div>
                    <h3 className="font-bold">{group.name}</h3>
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <Users className="w-4 h-4" />
                      <span>{group.members}</span>
                    </div>
                  </div>
                </div>
                <Button
                  onClick={() => setActiveGroup(group.name)}
                  className="bg-yellow-400 hover:bg-yellow-500 text-black font-semibold"
                >
                  Join Chat
                </Button>
              </div>
            </Card>
          ))}
        </div>

        {/* Leaderboard Preview */}
        <Card className="p-4">
          <h3 className="font-semibold mb-4">Top RAMblers</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-pink-400 flex items-center justify-center text-white text-sm font-medium">
                  S
                </div>
                <span className="font-medium">Sarah M.</span>
              </div>
              <span className="font-semibold">2,880</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-blue-400 flex items-center justify-center text-white text-sm font-medium">
                  M
                </div>
                <span className="font-medium">Mike R.</span>
              </div>
              <span className="font-semibold">2,720</span>
            </div>
          </div>
        </Card>
      </div>

      {/* Bottom Navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-yellow-400 p-2">
        <div className="flex justify-around items-center">
          <Button
            variant="ghost"
            size="sm"
            className="flex flex-col items-center gap-1 text-black"
            onClick={() => router.push("/dashboard")}
          >
            <Home className="w-5 h-5" />
            <span className="text-xs">HOME</span>
          </Button>
          <Button variant="ghost" size="sm" className="flex flex-col items-center gap-1 text-black">
            <Users className="w-5 h-5" />
            <span className="text-xs">GROUPS</span>
          </Button>
          <Button
            variant="ghost"
            size="sm"
            className="flex flex-col items-center gap-1 text-black"
            onClick={() => router.push("/leaderboard")}
          >
            <Trophy className="w-5 h-5" />
            <span className="text-xs">BOARD</span>
          </Button>
          <Button variant="ghost" size="sm" className="flex flex-col items-center gap-1 text-black">
            <MessageCircle className="w-5 h-5" />
            <span className="text-xs">PROFILE</span>
          </Button>
        </div>
      </div>
    </div>
  )
}
