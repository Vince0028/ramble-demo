"use client"

import { Button } from "@/components/ui/button"
import { useState } from "react"
import { useRouter } from "next/navigation"
import Image from "next/image"

export function QuizScreen() {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<string[]>([])
  const [timeLeft, setTimeLeft] = useState(10)
  const router = useRouter()

  const questions = [
    {
      question: "Your ideal weekend project involves:",
      options: [
        { icon: "⚙️", text: "Prototyping a new app idea" },
        { icon: "👥", text: "Organizing a hackathon" },
        { icon: "💻", text: "Learning a new programming language" },
        { icon: "📊", text: "Creating a business plan" },
      ],
    },
    {
      question: "What brings you to this event?",
      options: [
        { icon: "🤝", text: "Find mentors and advisors" },
        { icon: "💡", text: "Share my startup idea" },
        { icon: "🔗", text: "Network with like-minded people" },
        { icon: "📚", text: "Learn from industry experts" },
      ],
    },
    {
      question: "Choose your superpower:",
      options: [
        { icon: "💡", text: "Ideas - I'm the visionary" },
        { icon: "👥", text: "People - I connect and inspire" },
        { icon: "🔨", text: "Building - I make things happen" },
        { icon: "📈", text: "Strategy - I plan and execute" },
      ],
    },
  ]

  const handleAnswer = (answer: string) => {
    const newAnswers = [...answers, answer]
    setAnswers(newAnswers)

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
      setTimeLeft(10)
    } else {
      // Quiz completed, redirect to dashboard
      router.push("/dashboard")
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
      {/* Header */}
      <div className="p-4">
        <div className="flex items-center justify-between mb-4">
          <div className="text-sm">Pop-Up Quiz</div>
          <div className="flex items-center gap-2">
            <div className="text-sm">{timeLeft}s</div>
            <div className="w-8 h-1 bg-gray-600 rounded">
              <div
                className="h-full bg-yellow-400 rounded transition-all duration-1000"
                style={{ width: `${(timeLeft / 10) * 100}%` }}
              />
            </div>
          </div>
        </div>

        {/* Progress */}
        <div className="flex gap-1 mb-6">
          {questions.map((_, index) => (
            <div
              key={index}
              className={`flex-1 h-1 rounded ${index <= currentQuestion ? "bg-blue-500" : "bg-gray-600"}`}
            />
          ))}
        </div>
      </div>

      {/* Question */}
      <div className="flex-1 flex flex-col items-center justify-center p-6">
        {/* Logo */}
        <div className="w-24 h-24 mb-8">
          <Image src="/images/ramble-logo.png" alt="RAMBLE Logo" width={96} height={96} />
        </div>

        <h2 className="text-2xl font-bold text-center mb-8 text-balance">{questions[currentQuestion].question}</h2>

        {/* Options */}
        <div className="w-full max-w-sm space-y-4">
          {questions[currentQuestion].options.map((option, index) => (
            <Button
              key={index}
              onClick={() => handleAnswer(option.text)}
              className="w-full p-4 bg-white hover:bg-gray-100 text-black text-left flex items-center gap-3 rounded-xl"
            >
              <span className="text-xl">{option.icon}</span>
              <span className="font-medium">{option.text}</span>
            </Button>
          ))}
        </div>
      </div>

      {/* Question Counter */}
      <div className="p-4 text-center text-sm text-gray-400">
        {currentQuestion + 1}/{questions.length}
      </div>
    </div>
  )
}
