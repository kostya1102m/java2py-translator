class ComplexExample {
    private int counter = 0;
    public static final int MAX_VALUE = 100;
    public void incrementCounter(int step) {
        counter = counter + step;
        if (counter > MAX_VALUE) {
            counter = MAX_VALUE;
        }
    }
    private static int computeSum(int a, int b) {
        int result = a + b;
        for (int i = 0; i < 5; i = i + 1) {
            result = result * 2;
        }
        return result;
    }
    public String processData(int limit) {
        String message = "Processing";
        int temp = 0;
        while (temp < limit) {
            temp = temp + computeSum(temp, 1);
            message = message + " " + temp;
        }
        return message;
    }
    public static void main() {
        ComplexExample example = new ComplexExample();
        example.incrementCounter(10);
        int sum = computeSum(3, 4);
        String output = example.processData(sum);
    }
}