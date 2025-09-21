"use client"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { Users, Trophy, MessageCircle, Home, Crown, Medal, Award } from "lucide-react"

export function LeaderboardScreen() {
  const [selectedPeriod, setSelectedPeriod] = useState("week")
  const router = useRouter()

  const leaderboardData = [
    { name: "Qelvin N.", points: 6900, initial: "Q", rank: 1, badge: "🏆" },
    { name: "Rick C.", points: 4200, initial: "R", rank: 2, badge: "🥈" },
    { name: "Sarah M.", points: 2880, initial: "S", rank: 3, badge: "🥉" },
    { name: "Mike R.", points: 2720, initial: "M", rank: 4, badge: "" },
    { name: "Marwin G.", points: 2690, initial: "M", rank: 5, badge: "" },
    { name: "Alex (You)", points: 2690, initial: "A", rank: 4, badge: "", isCurrentUser: true },
    { name: "Christian B.", points: 2100, initial: "C", rank: 7, badge: "" },
    { name: "Vince A.", points: 1950, initial: "V", rank: 8, badge: "" },
    { name: "Carl B.", points: 1800, initial: "C", rank: 9, badge: "" },
    { name: "John D.", points: 1650, initial: "J", rank: 10, badge: "" },
  ]

  const periods = [
    { key: "day", label: "Today" },
    { key: "week", label: "This Week" },
    { key: "month", label: "This Month" },
    { key: "all", label: "All Time" },
  ]

  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1:
        return <Crown className="w-5 h-5 text-yellow-500" />
      case 2:
        return <Medal className="w-5 h-5 text-gray-400" />
      case 3:
        return <Award className="w-5 h-5 text-orange-500" />
      default:
        return <span className="text-lg font-bold text-gray-600">#{rank}</span>
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-blue-900 text-white p-4">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-bold flex items-center gap-2">
            <Trophy className="w-6 h-6" />
            Leaderboard
          </h1>
        </div>
      </div>

      <div className="p-4 space-y-4">
        {/* Period Selector */}
        <Card className="p-4">
          <div className="flex gap-2 overflow-x-auto">
            {periods.map((period) => (
              <Button
                key={period.key}
                variant={selectedPeriod === period.key ? "default" : "outline"}
                size="sm"
                onClick={() => setSelectedPeriod(period.key)}
                className={
                  selectedPeriod === period.key ? "bg-yellow-400 hover:bg-yellow-500 text-black" : "border-gray-300"
                }
              >
                {period.label}
              </Button>
            ))}
          </div>
        </Card>

        {/* Top 3 Podium */}
        <Card className="p-6">
          <h3 className="font-semibold mb-4 text-center">Top RAMblers</h3>
          <div className="flex justify-center items-end gap-4 mb-6">
            {/* 2nd Place */}
            <div className="text-center">
              <div className="w-16 h-16 bg-gray-400 rounded-full flex items-center justify-center text-white text-xl font-bold mb-2">
                {leaderboardData[1].initial}
              </div>
              <div className="text-2xl mb-1">🥈</div>
              <div className="font-semibold text-sm">{leaderboardData[1].name}</div>
              <div className="text-xs text-gray-600">{leaderboardData[1].points.toLocaleString()}</div>
            </div>

            {/* 1st Place */}
            <div className="text-center">
              <div className="w-20 h-20 bg-yellow-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mb-2">
                {leaderboardData[0].initial}
              </div>
              <div className="text-3xl mb-1">🏆</div>
              <div className="font-bold">{leaderboardData[0].name}</div>
              <div className="text-sm text-gray-600">{leaderboardData[0].points.toLocaleString()}</div>
            </div>

            {/* 3rd Place */}
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-500 rounded-full flex items-center justify-center text-white text-xl font-bold mb-2">
                {leaderboardData[2].initial}
              </div>
              <div className="text-2xl mb-1">🥉</div>
              <div className="font-semibold text-sm">{leaderboardData[2].name}</div>
              <div className="text-xs text-gray-600">{leaderboardData[2].points.toLocaleString()}</div>
            </div>
          </div>
        </Card>

        {/* Full Rankings */}
        <Card className="p-4">
          <h3 className="font-semibold mb-4">Full Rankings</h3>
          <div className="space-y-3">
            {leaderboardData.map((user, index) => (
              <div
                key={index}
                className={`flex items-center justify-between p-3 rounded-lg ${
                  user.isCurrentUser ? "bg-blue-50 border-2 border-blue-200" : "bg-white border border-gray-200"
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 flex items-center justify-center">{getRankIcon(user.rank)}</div>
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center text-white font-medium ${
                      user.rank === 1
                        ? "bg-yellow-500"
                        : user.rank === 2
                          ? "bg-gray-400"
                          : user.rank === 3
                            ? "bg-orange-500"
                            : user.isCurrentUser
                              ? "bg-blue-500"
                              : [
                                  "bg-pink-400",
                                  "bg-green-400",
                                  "bg-purple-400",
                                  "bg-indigo-400",
                                  "bg-red-400",
                                  "bg-teal-400",
                                ][index % 6]
                    }`}
                  >
                    {user.initial}
                  </div>
                  <div>
                    <div className={`font-medium ${user.isCurrentUser ? "text-blue-700" : ""}`}>
                      {user.name}
                      {user.isCurrentUser && <Badge className="ml-2 bg-blue-100 text-blue-800">You</Badge>}
                    </div>
                    <div className="text-sm text-gray-600">{user.points.toLocaleString()} Ram Points</div>
                  </div>
                </div>
                <div className="text-right">
                  {user.badge && <div className="text-2xl">{user.badge}</div>}
                  {user.rank <= 3 && (
                    <Badge
                      className={
                        user.rank === 1
                          ? "bg-yellow-100 text-yellow-800"
                          : user.rank === 2
                            ? "bg-gray-100 text-gray-800"
                            : "bg-orange-100 text-orange-800"
                      }
                    >
                      Top {user.rank}
                    </Badge>
                  )}
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Stats Card */}
        <Card className="p-4">
          <h3 className="font-semibold mb-4">Your Stats</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-3 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">#4</div>
              <div className="text-sm text-gray-600">Current Rank</div>
            </div>
            <div className="text-center p-3 bg-orange-50 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">2,690</div>
              <div className="text-sm text-gray-600">Total Points</div>
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
          <Button variant="ghost" size="sm" className="flex flex-col items-center gap-1 text-black bg-black/10">
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
    </div>
  )
}
