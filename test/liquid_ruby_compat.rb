# frozen_string_literal: true

# github-pages 222 pins Liquid 4.0.3, which still calls Ruby's former object
# taint APIs. Ruby 3.2 removed those no-op APIs, so local builds on modern Ruby
# need this small compatibility layer. GitHub's Pages build image is unaffected.
class Object
  def taint
    self
  end unless method_defined?(:taint)

  def untaint
    self
  end unless method_defined?(:untaint)

  def tainted?
    false
  end unless method_defined?(:tainted?)
end
