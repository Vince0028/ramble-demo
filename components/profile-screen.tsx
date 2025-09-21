"use client"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Users, Trophy, MessageCircle, Home, Settings, Star, Award } from "lucide-react"

interface RambleUser {
  name: string
  email: string
  points: number
  rank: number
}

export function ProfileScreen() {
  const [user, setUser] = useState<RambleUser | null>(null)
  const router = useRouter()

  useEffect(() => {
    const userData = localStorage.getItem("ramble_user")
    if (userData) {
      setUser(JSON.parse(userData))
    } else {
      router.push("/")
    }
  }, [router])

  const achievements = [
    { name: "First Connection", icon: "🤝", earned: true },
    { name: "Chat Master", icon: "💬", earned: true },
    { name: "Challenge Crusher", icon: "⚡", earned: false },
    { name: "Networking Ninja", icon: "🥷", earned: false },
  ]

  const interests = ["AI & Machine Learning", "Startup Ecosystem", "No-Code Tools", "Design Thinking"]

  const recentConnections = [
    { name: "Sarah M.", role: "UX Designer", mutual: 2 },
    { name: "Mike R.", role: "Full Stack Dev", mutual: 1 },
    { name: "Qelvin N.", role: "AI Researcher", mutual: 3 },
  ]

  if (!user) return null

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-blue-900 text-white p-4">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-bold">Profile</h1>
          <Button variant="ghost" size="sm">
            <Settings className="w-5 h-5" />
          </Button>
        </div>
      </div>

      <div className="p-4 space-y-4">
        {/* Profile Card */}
        <Card className="p-6 text-center">
          <div className="w-20 h-20 bg-blue-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
            {user.name.charAt(0)}
          </div>
          <h2 className="text-xl font-bold mb-1">{user.name}</h2>
          <p className="text-gray-600 mb-4">{user.email}</p>

          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-blue-600">#{user.rank}</div>
              <div className="text-sm text-gray-600">Rank</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-orange-500">{user.points.toLocaleString()}</div>
              <div className="text-sm text-gray-600">Points</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-500">12</div>
              <div className="text-sm text-gray-600">Connections</div>
            </div>
          </div>
        </Card>

        {/* Achievements */}
        <Card className="p-4">
          <h3 className="font-semibold mb-4 flex items-center gap-2">
            <Award className="w-5 h-5" />
            Achievements
          </h3>
          <div className="grid grid-cols-2 gap-3">
            {achievements.map((achievement, index) => (
              <div
                key={index}
                className={`p-3 rounded-lg border text-center ${
                  achievement.earned ? "bg-yellow-50 border-yellow-200" : "bg-gray-50 border-gray-200 opacity-50"
                }`}
              >
                <div className="text-2xl mb-1">{achievement.icon}</div>
                <div className="text-xs font-medium">{achievement.name}</div>
              </div>
            ))}
          </div>
        </Card>

        {/* Interests */}
        <Card className="p-4">
          <h3 className="font-semibold mb-4 flex items-center gap-2">
            <Star className="w-5 h-5" />
            Interests
          </h3>
          <div className="flex flex-wrap gap-2">
            {interests.map((interest, index) => (
              <Badge key={index} variant="secondary" className="bg-blue-100 text-blue-800">
                {interest}
              </Badge>
            ))}
          </div>
        </Card>

        {/* Recent Connections */}
        <Card className="p-4">
          <h3 className="font-semibold mb-4 flex items-center gap-2">
            <Users className="w-5 h-5" />
            Recent Connections
          </h3>
          <div className="space-y-3">
            {recentConnections.map((connection, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center text-white font-medium ${
                      ["bg-pink-400", "bg-blue-400", "bg-green-400"][index]
                    }`}
                  >
                    {connection.name.charAt(0)}
                  </div>
                  <div>
                    <div className="font-medium">{connection.name}</div>
                    <div className="text-sm text-gray-600">{connection.role}</div>
                  </div>
                </div>
                <div className="text-xs text-gray-500">{connection.mutual} mutual</div>
              </div>
            ))}
          </div>
        </Card>

        {/* Event History */}
        <Card className="p-4">
          <h3 className="font-semibold mb-4">Event History</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <div className="font-medium">AI Innovators Summit</div>
                <div className="text-sm text-gray-600">Sept 21, 2025</div>
              </div>
              <Badge className="bg-green-100 text-green-800">Completed</Badge>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <div className="font-medium">Tech Startup Mixer</div>
                <div className="text-sm text-gray-600">Sept 15, 2025</div>
              </div>
              <Badge className="bg-green-100 text-green-800">Completed</Badge>
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
          <Button
            variant="ghost"
            size="sm"
            className="flex flex-col items-center gap-1 text-black"
            onClick={() => router.push("/groups")}
          >
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
