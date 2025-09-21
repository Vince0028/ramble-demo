"use client"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { X, Trophy } from "lucide-react"

interface ChallengeModalProps {
  isOpen: boolean
  onClose: () => void
  challenge: {
    title: string
    description: string
    points: number
    timeLimit: string
  }
}

export function ChallengeModal({ isOpen, onClose, challenge }: ChallengeModalProps) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <Card className="w-full max-w-sm bg-yellow-400 text-black">
        <div className="p-6">
          <div className="flex items-center justify-between mb-4">
            <Trophy className="w-6 h-6" />
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="w-4 h-4" />
            </Button>
          </div>

          <h3 className="text-xl font-bold mb-2">{challenge.title}</h3>
          <p className="text-sm mb-4">{challenge.description}</p>

          <div className="flex items-center justify-between mb-6">
            <div className="text-sm">
              <span className="font-semibold">Earn: {challenge.points} points</span>
            </div>
            <div className="text-sm">
              <span className="font-semibold">Time: {challenge.timeLimit}</span>
            </div>
          </div>

          <div className="space-y-3">
            <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold">Accept Challenge</Button>
            <Button variant="outline" className="w-full bg-transparent" onClick={onClose}>
              Maybe Later
            </Button>
          </div>
        </div>
      </Card>
    </div>
  )
}
