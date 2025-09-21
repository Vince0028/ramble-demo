"use client"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { useState } from "react"
import { useRouter } from "next/navigation"
import Image from "next/image"

export function LoginScreen() {
  const [email, setEmail] = useState("")
  const router = useRouter()

  const handleEmailSignup = () => {
    if (email) {
      // Store user info in localStorage for demo
      localStorage.setItem(
        "ramble_user",
        JSON.stringify({
          name: "Alex",
          email: email,
          points: 2690,
          rank: 4,
        }),
      )
      router.push("/dashboard")
    }
  }

  const handleLinkedInLogin = () => {
    // Store demo user info
    localStorage.setItem(
      "ramble_user",
      JSON.stringify({
        name: "Alex",
        email: "alex@example.com",
        points: 2690,
        rank: 4,
      }),
    )
    router.push("/dashboard")
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-yellow-400 to-yellow-500 flex items-center justify-center p-4">
      <Card className="w-full max-w-sm bg-gradient-to-b from-yellow-400 to-yellow-500 border-none shadow-none">
        <div className="p-8 text-center space-y-8">
          {/* Logo */}
          <div className="flex justify-center">
            <div className="w-32 h-32 relative">
              <Image src="/images/ramble-logo.png" alt="RAMBLE Logo" fill className="object-contain" />
            </div>
          </div>

          {/* Login Buttons */}
          <div className="space-y-4">
            <Button
              onClick={handleLinkedInLogin}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded-lg"
            >
              Continue with LinkedIn
            </Button>

            <div className="text-white font-medium">OR</div>

            <div className="space-y-3">
              <Input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-white border-none rounded-lg py-3 px-4 text-gray-900 placeholder-gray-500"
              />
              <Button
                onClick={handleEmailSignup}
                className="w-full bg-white hover:bg-gray-100 text-gray-900 font-medium py-3 rounded-lg"
              >
                📧 Sign up with Email
              </Button>
            </div>
          </div>
        </div>
      </Card>
    </div>
  )
}
