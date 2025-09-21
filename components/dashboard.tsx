"use client"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Users, Clock, Trophy, MessageCircle, Home } from "lucide-react"
import { ChallengeModal } from "./challenge-modal"

interface RambleUser {
  name: string
  email: string
  points: number
  rank: number
}

export function Dashboard() {
  const [user, setUser] = useState<RambleUser | null>(null)
  const [timeToNextRound, setTimeToNextRound] = useState(7 * 60) // 7 minutes in seconds
  const [showChallenge, setShowChallenge] = useState(false)
  const router = useRouter()

  const challenge = {
    title: "Network Challenge!",
    description: "Talk to 3 designers in 20 minutes and discover their favorite design tools!",
    points: 50,
    timeLimit: "20 mins",
  }

  useEffect(() => {
    const userData = localStorage.getItem("ramble_user")
    if (userData) {
      setUser(JSON.parse(userData))
    } else {
      router.push("/")
    }

    // Show challenge after 3 seconds
    const timer = setTimeout(() => {
      setShowChallenge(true)
    }, 3000)

    return () => clearTimeout(timer)
  }, [router])

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeToNextRound((prev) => (prev > 0 ? prev - 1 : 0))
    }, 1000)
    return () => clearInterval(timer)
  }, [])

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, "0")}`
  }

  const topRamblers = [
    { name: "Sarah M.", points: 2880, initial: "S" },
    { name: "Mike R.", points: 2720, initial: "M" },
    { name: "Qelvin N.", points: 6900, initial: "Q" },
    { name: "Rick C.", points: 4200, initial: "R" },
    { name: "Marwin G.", points: 2690, initial: "M" },
  ]

  const upcomingRounds = [
    { name: "No-Code Builders", time: "45 mins" },
    { name: "Crypto Enthusiast", time: "2 hours" },
  ]

  if (!user) return null

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-blue-900 text-white p-4 text-center">
        <div className="flex items-center justify-center gap-2 mb-2">
          <span>👋</span>
          <span className="font-semibold">Hi, {user.name}!</span>
        </div>
        <div className="text-sm opacity-90">Your first round starts in {formatTime(timeToNextRound)}</div>
      </div>

      <div className="p-4 space-y-4">
        {/* Event Card */}
        <Card className="p-4">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="font-bold text-lg">AI Innovators</h2>
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Users className="w-4 h-4" />
                <span>4/6 Rams</span>
                <Clock className="w-4 h-4 ml-2" />
                <span>{formatTime(timeToNextRound)}</span>
              </div>
            </div>
            <div className="flex -space-x-2">
              {["S", "M", "A", "J", "C", "Y"].map((initial, i) => (
                <div
                  key={i}
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium text-white ${
                    ["bg-pink-400", "bg-blue-400", "bg-green-400", "bg-purple-400", "bg-orange-400", "bg-yellow-400"][i]
                  }`}
                >
                  {initial}
                </div>
              ))}
            </div>
          </div>
          <Button
            className="w-full bg-yellow-400 hover:bg-yellow-500 text-black font-semibold py-3"
            onClick={() => router.push("/quiz")}
          >
            Join Now! ⚡
          </Button>
        </Card>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 gap-4">
          <Card className="p-4 text-center">
            <Trophy className="w-6 h-6 mx-auto mb-2 text-orange-500" />
            <div className="text-2xl font-bold">#{user.rank}</div>
            <div className="text-sm text-gray-600">This week</div>
          </Card>
          <Card className="p-4 text-center">
            <div className="text-2xl font-bold text-orange-500">{user.points.toLocaleString()}</div>
            <div className="text-sm text-gray-600">Ram Points</div>
          </Card>
        </div>

        {/* Top RAMblers */}
        <Card className="p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold">Top RAMblers</h3>
            <Button variant="ghost" size="sm" className="text-blue-600">
              View All
            </Button>
          </div>
          <div className="space-y-3">
            {topRamblers.slice(0, 3).map((rambler, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-medium ${
                      ["bg-pink-400", "bg-blue-400", "bg-green-400"][index]
                    }`}
                  >
                    {rambler.initial}
                  </div>
                  <span className="font-medium">{rambler.name}</span>
                </div>
                <span className="font-semibold">{rambler.points.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </Card>

        {/* Upcoming Rounds */}
        <Card className="p-4">
          <h3 className="font-semibold mb-4">Upcoming Rounds</h3>
          <div className="space-y-3">
            {upcomingRounds.map((round, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span className="font-medium">{round.name}</span>
                <span className="text-sm text-gray-600">{round.time}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Bottom Navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-yellow-400 p-2">
        <div className="flex justify-around items-center">
          <Button variant="ghost" size="sm" className="flex flex-col items-center gap-1 text-black">
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
          <Button
            variant="ghost"
            size="sm"
            className="flex flex-col items-center gap-1 text-black"
            onClick={() => router.push("/profile")}
          >
            <MessageCircle className="w-5 h-5" />
            <span className="text-xs">PROFILE</span>
          </Button>
        </div>
      </div>

      {/* Challenge Modal */}
      <ChallengeModal isOpen={showChallenge} onClose={() => setShowChallenge(false)} challenge={challenge} />
    </div>
  )
}
